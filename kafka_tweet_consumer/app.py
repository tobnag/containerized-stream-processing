import os
from json import loads 
from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = f"{os.environ['KAFKA_ADVERTISED_HOST_NAME']}:{os.environ['KAFKA_PORT']}"
API_VERSION = tuple(map(lambda s: int(s.strip()), os.environ['KAFKA_API_VERSION'].split(',')))
TOPIC_TRUMP = os.environ['KAFKA_TOPIC_TRUMP']
TOPIC_BIDEN = os.environ['KAFKA_TOPIC_BIDEN']

consumer = KafkaConsumer(
    TOPIC_TRUMP,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    api_version=API_VERSION,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

if __name__ == '__main__':
    for i, message in enumerate(consumer):
        print(f"Message received (#{i+1}): [{message.topic}] {message.value}")
        