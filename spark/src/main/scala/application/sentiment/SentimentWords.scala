package application.sentiment

import scala.io.Source
import scala.io.Codec.UTF8

/**
 * Object containing the positive and negative words used for sentiment analysis
 */
object SentimentWords {
  val positiveWords: Set[String] = readWords("positive-words.txt")
  val negativeWords: Set[String] = readWords("negative-words.txt")
  
  private def readWords(fileName: String): Set[String] = {
    val inputStream = getClass.getClassLoader.getResourceAsStream(fileName)
    val source = Source.fromInputStream(inputStream)(UTF8)
    val lines = source.getLines()
      .map(_.trim)
      .filterNot(line => line.isEmpty || line.startsWith("#"))
      .toSet
    source.close()
    lines
  }
}
