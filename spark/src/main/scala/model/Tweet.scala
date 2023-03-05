package model

import java.sql.Timestamp

/**
 * This class models a Tweet.
 */
case class Tweet(
  created_at: Timestamp,
  tweet_id: Long,
  tweet: String
)

/**
 * This object contains a method to parse a string into a Tweet object.
 */
 object Tweet {
  def parse(line: String): Option[Tweet] = {
    val fields = line.split("\t")
    try {     
      Some(Tweet(
        Timestamp.valueOf(fields(0)),
        fields(1).toLong,
        fields(2)
      ))
    } catch {
      case ex: IndexOutOfBoundsException =>
        Console.err.println(s"$ex: line = $line")
        None
    }
  }
 }