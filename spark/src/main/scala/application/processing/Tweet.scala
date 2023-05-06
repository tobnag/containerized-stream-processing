package application.processing

import java.sql.Timestamp

/**
 * This class models a Tweet as it is provided by the data stream.
 */
case class Tweet(
  created_at: Timestamp,
  tweet_id: Long,
  tweet: String,
  likes: Int,
  retweet_count: Int,
  source: String,
  user_id: Long,
  user_name: String,
  user_screen_name: String,
  user_description: String,
  user_join_date: Timestamp,
  user_followers_count: Int,
  user_location: String,
  lat: Double,
  lon: Double,
  city: String,
  country: String,
  continent: String,
  state: String,
  state_code: String,
  collected_at: Timestamp
) {
  def process(candidate: String): ProcessedTweet = {
    val analysis = Analysis(this)
    ProcessedTweet(candidate, analysis, this)
  }
}

/**
 * This class models a processed Tweet as it is provided to the analytics service.
 */
case class ProcessedTweet(
    candidate: String,   // respective presidential candidate
    analysis: Analysis,  // different analytical insights
    tweet: Tweet,        // original tweet with metadata
)