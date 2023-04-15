package application.model

import java.util.Properties
import scala.collection.JavaConverters._
import edu.stanford.nlp.pipeline._
import edu.stanford.nlp.ling.CoreAnnotations
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations

object SentimentPipeline {
  private val props = new Properties()
  props.setProperty("annotators", "tokenize, pos, parse, sentiment")
  private val pipeline = new StanfordCoreNLP(props)

  def apply(): StanfordCoreNLP = pipeline
}

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
    val text = tweet.tweet
    val annotation = SentimentPipeline().process(text)
    val sentences = annotation.get(classOf[CoreAnnotations.SentencesAnnotation]).asScala.toList
    val sentiment = sentences.map(_.get(classOf[SentimentCoreAnnotations.SentimentAnnotatedTree]))
      .map(_.score())
      .reduce((a, b) => a + b) / sentences.length
    // scale sentiment to [-2, 2], which means [negative, positive]
    sentiment - 2
  }
}