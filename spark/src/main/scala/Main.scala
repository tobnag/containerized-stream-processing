import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.Trigger

object KafkaStreamExample {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder
      .appName("KafkaStreamExample")
      .master("spark://spark-master:7077")
      .getOrCreate()

    import spark.implicits._

    val kafkaParams = Map[String, String](
      "kafka.bootstrap.servers" -> "kafka:9092",
      "subscribe" -> "trump,biden"
    )

    val streamDF = spark.readStream
      .format("kafka")
      .options(kafkaParams)
      .load()

    val messagesDF = streamDF.selectExpr("CAST(value AS STRING)")

    val query = messagesDF.writeStream
      .outputMode("append")
      .format("console")
      .trigger(Trigger.ProcessingTime("10 seconds"))
      .start()

    query.awaitTermination()
  }
}
