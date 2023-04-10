package model

case class Analysis(
  charCount: Int,
  wordCount: Int
)

object Analysis {

  def apply(tweet: Tweet): Analysis = {
    val charCount = charCountAnalysis(tweet)
    val wordCount = wordCountAnalysis(tweet)
    Analysis(charCount, wordCount)
  }

  def charCountAnalysis(tweet: Tweet): Int = tweet.tweet.length
  def wordCountAnalysis(tweet: Tweet): Int = tweet.tweet.split(" ").length
}