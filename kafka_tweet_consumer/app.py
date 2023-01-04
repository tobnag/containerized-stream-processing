import json 
from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = ['kafka:9092']
API_VERSION = (0, 10, 2)
TOPIC = 'trump'

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    api_version=API_VERSION
)

if __name__ == '__main__':
    for i, message in enumerate(consumer):
        print(f"Message received (#{i+1}): {json.loads(message.value)}")
        