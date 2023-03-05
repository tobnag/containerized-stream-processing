import os

BOOTSTRAP_SERVERS = f"{os.environ['KAFKA_ADVERTISED_HOST_NAME']}:{os.environ['KAFKA_PORT']}"
API_VERSION = tuple(map(lambda s: int(s.strip()), os.environ['KAFKA_API_VERSION'].split(',')))
TOPIC_TRUMP = os.environ['KAFKA_TOPIC_TRUMP']
TOPIC_BIDEN = os.environ['KAFKA_TOPIC_BIDEN']
PATH_TRUMP = os.environ['FILE_PATH_TRUMP']
PATH_BIDEN = os.environ['FILE_PATH_BIDEN']
