# Build stage
FROM sbtscala/scala-sbt:eclipse-temurin-jammy-8u352-b08_1.8.2_2.12.17 AS builder
WORKDIR /app
COPY ./build.sbt .
COPY ./project ./project
RUN sbt update
COPY ./src ./src
RUN sbt package

# Runtime stage
FROM bitnami/spark:3.3.2
COPY --from=builder /app/target/scala-2.12/kafkasparkstructuredstreaming_2.12-0.1.jar /app/SparkApp.jar
CMD ["/opt/bitnami/spark/bin/spark-submit", "--master", "spark://spark-master:7077", "/app/SparkApp.jar"]

# Spark package for Kafka 0.10:
# --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2