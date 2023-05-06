package application.processing

import scala.util.matching.Regex
import application.sentiment.SentimentWords.{positiveWords, negativeWords}

/**
 * Case class representing the result of tweet analysis
 *
 * @param hashtags  List of hashtags found in the tweet
 * @param hasUrl    Boolean indicating whether the tweet contains a URL
 * @param sentiment Integer representing the sentiment of the tweet
 *                  (ranging from -2 to 2, where -2 is very negative and 2 is very positive)
 */
case class Analysis(
  hashtags: List[String],
  hasUrl: Boolean,
  sentiment: Int
)

/**
 * Companion object to the Analysis case class
 */
object Analysis {

  def apply(tweet: Tweet): Analysis = {
    val text = Option(tweet.tweet).getOrElse("")
    val hashtags: List[String] = extractHashtags(text)
    val hasUrl: Boolean = extractHasUrl(text)
    val sentiment: Int = extractSentiment(text)
    Analysis(hashtags, hasUrl, sentiment)
  }

  private val hashtagPattern: Regex = "#[\\w-]+".r
  private val urlPattern: Regex = "https?://\\S+|www\\.\\S+".r
  
  private def extractHashtags(text: String): List[String] = {
    hashtagPattern.findAllIn(text).toList
  }

  private def extractHasUrl(text: String): Boolean = {
    urlPattern.findFirstMatchIn(text).isDefined
  }

  private val patternsToRemove: Seq[Regex] = Seq(
    urlPattern, // remove URLs
    hashtagPattern, // remove hashtags
    "@[\\w-]+".r, // remove mentions
    "\\[.*?\\]".r, // remove square brackets
    "<.*?>+".r, // remove HTML tags
    "&.*?;".r, // remove HTML entities
    "\\n".r, // remove new lines
    "\\d+".r, // remove numbers
    "RT[\\s]+".r, // remove retweet tags
    "[^\\w]".r // remove punctuation
  )

  private def cleanText(text: String): String = {
    patternsToRemove.foldLeft(text.toLowerCase()) { (cleanedText, pattern) => // lower case
      pattern.replaceAllIn(cleanedText, " ") // replace defined patterns with a whitespace
    }.replaceAll("\\s+", " ").trim() // finally, remove unnecessary whitespaces
  }
  
  private def extractSentiment(text: String): Int = {
    val cleanedText = cleanText(text)
    val cleanedWords = cleanedText.split(" ")
    val posWordCount = cleanedWords.count(positiveWords.contains) // use predefined positive words
    val negWordCount = cleanedWords.count(negativeWords.contains) // use predefined negative words
    val sentiment = posWordCount - negWordCount
    math.min(2, math.max(-2, sentiment)) // limit sentiment to range [-2, 2] --> [very negative, very positive]
  }
}