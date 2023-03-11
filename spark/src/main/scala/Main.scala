import org.apache.spark.sql.{SparkSession, Dataset, Encoders}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.Trigger
import model._

object Main {

  def main(args: Array[String]): Unit = {

    // Create a SparkSession
    val spark = SparkSession.builder
      .appName("SparkStructuredStreamingApp")
      .master("spark://spark-master:7077")
      .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    // Import implicits to use the $-notation
    import spark.implicits._

    // Stream messages from Kafka
    val kafkaParams = Map[String, String](
      "kafka.bootstrap.servers" -> "kafka:9092",
      "subscribe" -> "trump,biden",
      "startingOffsets" -> "earliest"
    )
    val streamDF = spark.readStream
      .format("kafka")
      .options(kafkaParams)
      .load()

    // Stream tweets and cast them according to the Tweet class schema
    val schema = Encoders.product[Tweet].schema
    val tweets: Dataset[Tweet] = streamDF
      .selectExpr("CAST(value AS STRING)").as[String]
      .select(from_json($"value", schema).alias("tweets"))
      .select("tweets.*")
      .as[Tweet]

    // Print results on the console
    val consoleOutput = tweets.writeStream
      .format("console")
      .option("truncate", "false")
      .trigger(Trigger.ProcessingTime("1 seconds"))
      .start()
    consoleOutput.awaitTermination()
  }
}
