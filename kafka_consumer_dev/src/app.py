import os
from json import loads 
from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = "kafka:9092"
API_VERSION = (0, 10, 2)

consumer = KafkaConsumer(
    'processed_tweets',
    bootstrap_servers=BOOTSTRAP_SERVERS,
    api_version=API_VERSION,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

if __name__ == '__main__':
    for i, message in enumerate(consumer):
        print(f"Message received (#{i+1}): [{message.topic}] {message.value}")
        