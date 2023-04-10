import org.apache.spark.sql.{SparkSession, DataFrame, Dataset, Encoders}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.Trigger
import model.{Tweet, ProcessedTweet}

object Main {

  // Environment variables and static class members
  private val KAFKA_BROKER = "kafka:9092"
  private val KAFKA_TOPIC_TRUMP = "trump"
  private val KAFKA_TOPIC_BIDEN = "biden"
  private val KAFKA_TOPIC_PROCESSED = "processed_tweets"
  private val NAME_TRUMP = "Donald Trump"
  private val NAME_BIDEN = "Joe Biden"

  def main(args: Array[String]): Unit = {
    // Create a SparkSession
    val spark = SparkSession.builder
      .appName("SparkStructuredStreamingApp")
      .master("spark://spark-master:7077")
      .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")
      .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    // Import implicits to use the $-notation
    import spark.implicits._

    // Stream messages from Kafka
    val loadStream = (topic: String) => spark.readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", KAFKA_BROKER)
      .option("subscribe", topic)
      .option("startingOffsets", "earliest")
      .load()
    val streamTrump: DataFrame = loadStream(KAFKA_TOPIC_TRUMP)
    val streamBiden: DataFrame = loadStream(KAFKA_TOPIC_BIDEN)

    // Stream tweets and cast them according to the Tweet class schema
    val schema = Encoders.product[Tweet].schema
    val readStream = (stream: DataFrame) => stream
      .selectExpr("CAST(value AS STRING)").as[String]
      .select(from_json($"value", schema).alias("tweets"))
      .select("tweets.*")
      .as[Tweet]
    val tweetsTrump: Dataset[Tweet] = streamTrump.transform(readStream)
    val tweetsBiden: Dataset[Tweet] = streamBiden.transform(readStream)

    // Process tweets
    val processedTweetsTrump: Dataset[ProcessedTweet] = tweetsTrump.map(_.process(NAME_TRUMP))
    val processedTweetsBiden: Dataset[ProcessedTweet] = tweetsBiden.map(_.process(NAME_BIDEN))

    // Merge streams of processed tweets for the analytics service
    val processedTweets: Dataset[ProcessedTweet] = processedTweetsTrump.union(processedTweetsBiden)

    // Write tweets to Kafka
    val kafkaOutput = processedTweets
      .select(to_json(struct($"*")).alias("value"))
      .writeStream
      .format("kafka")
      .option("kafka.bootstrap.servers", KAFKA_BROKER)
      .option("topic", KAFKA_TOPIC_PROCESSED)
      .option("checkpointLocation", "/tmp/kafka_outbound_checkpoint")
      .start()
    kafkaOutput.awaitTermination()
  }
}
