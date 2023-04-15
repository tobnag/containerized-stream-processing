import sbt.Keys._

// *****************************************************************************
// Project
// *****************************************************************************

name := "KafkaSparkStructuredStreaming"
version := "0.1"

lazy val sparkDoc = project
  .in(file("."))
  .settings(
    settings,
    libraryDependencies ++= Seq(
      library.spark,
      library.sparkCore,
      library.sparkSql,
      library.sparkStreaming,
      library.sparkStreamingKafka,
      library.sentimentAnalysis,
      library.sentimentAnalysisModels
    )
  )

// *****************************************************************************
// Dependency Settings
// *****************************************************************************

lazy val library = new {

  val version = new {
    val scala = "2.12.17"
    val spark = "3.3.2"
    val stanfordNLP = "4.5.3"
  }

  val spark = "org.apache.spark" %% "spark-sql-kafka-0-10" % version.spark
  val sparkCore = "org.apache.spark" %% "spark-core" % version.spark
  val sparkSql = "org.apache.spark" %% "spark-sql" % version.spark
  val sparkStreaming = "org.apache.spark" %% "spark-streaming" % version.spark
  val sparkStreamingKafka = "org.apache.spark" %% "spark-streaming-kafka-0-10" % version.spark
  val sentimentAnalysis = "edu.stanford.nlp" % "stanford-corenlp" % version.stanfordNLP
  val sentimentAnalysisModels = "edu.stanford.nlp" % "stanford-corenlp" % version.stanfordNLP classifier "models"
}

// *****************************************************************************
// Settings
// *****************************************************************************

lazy val settings = commonSettings

lazy val commonSettings = Seq(
  scalaVersion := library.version.scala,
)