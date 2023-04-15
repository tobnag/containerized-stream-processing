package application.model

import com.johnsnowlabs.nlp.pretrained.PretrainedPipeline
import org.apache.spark.sql.SparkSession

case class Analysis(
  charCount: Int,
  wordCount: Int,
  sentiment: Double,
)

object Analysis {

  def apply(tweet: Tweet): Analysis = {
    val charCount = charCountAnalysis(tweet)
    val wordCount = wordCountAnalysis(tweet)
    val sentiment = sentimentAnalysis(tweet)
    Analysis(charCount, wordCount, sentiment)
  }

  def charCountAnalysis(tweet: Tweet): Int = tweet.tweet.length
  def wordCountAnalysis(tweet: Tweet): Int = tweet.tweet.split(" ").length

  def sentimentAnalysis(tweet: Tweet): Double = {
    // Get the active spark session for further use without creating a new one.
    val spark = SparkSession.active
    println(s"Analysis: spark = $spark")
    import spark.implicits._

    // Create a dataframe with the tweet text
    val text = tweet.tweet
    val df = Seq(text).toDF("text")

    // Use a pretrained pipeline to get the sentiment of the tweet.
    val pipeline = PretrainedPipeline("analyze_sentimentdl_use_twitter", lang = "en").lightModel

    // Run the pipeline on the dataframe
    val annotation = pipeline.transform(df)

    annotation.show(false)
    
    // Get the sentiment score
    val sentiment = annotation.select("sentiment.result").collect()(0).get(0).toString.toDouble

    sentiment
  }
}
