import sbt.Keys._

// *****************************************************************************
// Project
// *****************************************************************************

name := "KafkaSparkStructuredStreaming"
version := "0.1"

lazy val acdcDoc = project
  .in(file("."))
  .settings(
    settings,
    libraryDependencies ++= Seq(
      library.spark
    )
  )

// *****************************************************************************
// Dependency Settings
// *****************************************************************************

lazy val library = new {

  val version = new {
    val scala = "2.12.17"
    val spark = "3.3.2"
  }

//   val spark = "org.apache.spark" %% "spark-sql" % version.spark
  val spark = "org.apache.spark" %% "spark-sql-kafka-0-10" % version.spark
}

// *****************************************************************************
// Settings
// *****************************************************************************

lazy val settings = commonSettings

lazy val commonSettings = Seq(
  scalaVersion := library.version.scala,
)