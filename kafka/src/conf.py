import os

# Datasets
COL_CREATED_AT = 'created_at'
COL_TOPIC = 'topic'
DTYPES = {
    'tweet_id': int,
    'likes': int,
    'retweet_count': int,
    'user_id': int,
    'user_followers_count': int,
    'lat': float,
    'long': float
}
PARSE_DATES = [COL_CREATED_AT, 'user_join_date', 'collected_at']
LINETERMINATOR = '\n'
DROP_NA = [COL_CREATED_AT, 'tweet']
DROP_DUPLICATES = [COL_CREATED_AT, 'tweet_id', 'user_id']
RENAME = {'long': 'lng'}  # long is a reserved keyword

# Kafka
BOOTSTRAP_SERVERS = f"{os.environ['KAFKA_ADVERTISED_HOST_NAME']}:{os.environ['KAFKA_PORT']}"
API_VERSION = tuple(map(lambda s: int(s.strip()), os.environ['KAFKA_API_VERSION'].split(',')))
TOPIC_TRUMP = os.environ['KAFKA_TOPIC_TRUMP']
TOPIC_BIDEN = os.environ['KAFKA_TOPIC_BIDEN']
PATH_TRUMP = os.environ['FILE_PATH_TRUMP']
PATH_BIDEN = os.environ['FILE_PATH_BIDEN']
ENCODER = 'utf-8'
