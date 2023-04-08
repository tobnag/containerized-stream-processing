import org.apache.spark.sql.{SparkSession, Dataset, Encoders}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.Trigger
import model._

object Main {

  // Create static class members for environment variables of Kafka topics. Variables should be static and final.
  private val KAFKA_BROKER = sys.env("KAFKA_ADVERTISED_HOST_NAME") + ":" + sys.env("KAFKA_PORT")
  private val KAFKA_TOPIC_TRUMP = sys.env("KAFKA_TOPIC_TRUMP")
  private val KAFKA_TOPIC_BIDEN = sys.env("KAFKA_TOPIC_BIDEN")
  private val KAFKA_TOPIC_PROCESSED = sys.env("KAFKA_TOPIC_PROCESSED")

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
    val streamDF = spark.readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", KAFKA_BROKER)
      .option("subscribe", KAFKA_TOPIC_TRUMP + "," + KAFKA_TOPIC_BIDEN)
      .option("startingOffsets", "earliest")
      .load()

    // Stream tweets and cast them according to the Tweet class schema
    val schema = Encoders.product[Tweet].schema
    val tweets: Dataset[Tweet] = streamDF
      .selectExpr("CAST(value AS STRING)").as[String]
      .select(from_json($"value", schema).alias("tweets"))
      .select("tweets.*")
      .as[Tweet]

    // Write tweets to Kafka
    val kafkaOutput = tweets
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
