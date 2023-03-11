package model

import java.sql.Timestamp

/**
 * This class models a Tweet.
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
  lng: Double,
  city: String,
  country: String,
  continent: String,
  state: String,
  state_code: String,
  collected_at: Timestamp
)