# Containerized Stream Processing with Docker - Tweet Analysis
[![Elastic Stack version](https://img.shields.io/badge/Elastic%20Stack-8.7.1-00bfb3?style=flat&logo=elastic-stack)](https://www.elastic.co/blog/category/releases)

This project implements a large-scale and data-intensive application for real-time stream processing.

The streaming pipeline consists of [Apache Kafka](https://kafka.apache.org), [Apache Spark](https://spark.apache.org), as well as [Logstash](https://www.elastic.co/logstash/), [Elasticsearch](https://www.elastic.co/elasticsearch/), and [Kibana](https://www.elastic.co/kibana/) from the [Elastic Stack](https://www.elastic.co/elastic-stack/). With the use of Docker, the solution stack is assembled with isolated microservices orchestrated by docker-compose. The layout ensures reliability, scalability, and maintainability.

As an example use case, a Twitter dataset about the 2020 United States presidential election is processed and visualized in a dashboard.

## Table of Contents
1. [Requirements](#requirements)
1. [Installation](#installation)
1. [Usage](#usage)
1. [Going Further](#going-further)
1. [Sources](#sources)
1. [License](#license)