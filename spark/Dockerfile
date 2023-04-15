ARG SPARK_VERSION

# First build stage: Download the CoreNLP library and pre-trained language models
FROM alpine:3.17.3 AS downloader
WORKDIR /opt
RUN apk update && apk add --no-cache wget unzip && \
    wget http://nlp.stanford.edu/software/stanford-corenlp-4.5.3.zip && \
    unzip stanford-corenlp-4.5.3.zip && \
    rm stanford-corenlp-4.5.3.zip
WORKDIR /opt/stanford-corenlp-4.5.3
RUN wget http://nlp.stanford.edu/software/stanford-corenlp-4.5.3-models-english.jar

# Second build stage: Build the Spark application with SBT from Scala source files
FROM sbtscala/scala-sbt:eclipse-temurin-jammy-8u352-b08_1.8.2_2.12.17 AS builder
WORKDIR /app
COPY ./build.sbt .
COPY ./project ./project
RUN sbt update
COPY ./src ./src
RUN sbt package

# Runtime stage
FROM bitnami/spark:${SPARK_VERSION}
COPY --from=downloader /opt/stanford-corenlp-4.5.3 /opt/stanford-corenlp-4.5.3
COPY --from=builder /app/target/scala-2.12/kafkasparkstructuredstreaming_2.12-0.1.jar /app/SparkApp.jar
CMD ["/opt/bitnami/spark/bin/spark-submit",\
     "--master", "spark://spark-master:7077",\
     "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2",\
     "--jars", "/opt/stanford-corenlp-4.5.3/*.jar",\
     "/app/SparkApp.jar"]