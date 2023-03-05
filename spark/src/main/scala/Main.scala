import org.apache.spark.sql._
import org.apache.spark.sql.functions._
import model._

object Main {

  def main(args: Array[String]): Unit = {

    // Create a SparkSession
    val spark = SparkSession.builder
      .appName("SparkStructuredStreamingApp")
      .master("spark://spark-master:7077")
      .getOrCreate()

    // Define the log-level for debbuging purposes
    spark.sparkContext.setLogLevel("WARN")

    // Import implicits to use the $-notation
    import spark.implicits._

    // Define parameters to read messages from Kafka
    val kafkaParams = Map[String, String](
      "kafka.bootstrap.servers" -> "kafka:9092",
      "subscribe" -> "trump,biden"
    )

    // Read messages from Kafka
    val streamDF = spark.readStream
      .format("kafka")
      .options(kafkaParams)
      .load()

    // Parse messages as Tweet objects
    val tweets: Dataset[Tweet] = streamDF
      .flatMap {
        case row if !row.isNullAt(0) && !row.isNullAt(1) && !row.isNullAt(2) =>
          Tweet.parse(row.mkString)
        case _ => None
      }

    // Print the result on the console
    val consoleOutput = tweets.writeStream
      .outputMode("update")
      .format("console")
      .start()

    // Wait for the termination signal
    consoleOutput.awaitTermination()
  }
}
