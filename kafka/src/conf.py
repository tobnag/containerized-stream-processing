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
DROP_NA = [COL_CREATED_AT, 'tweet_id', 'tweet']
DROP_DUPLICATES = [COL_CREATED_AT, COL_TOPIC, 'tweet_id']
FILL_NA_INT = ['likes', 'retweet_count', 'user_followers_count']
FILL_NA_INT_DEFAULT = -1
FILL_NA_FLOAT = ['lat', 'long']
FILL_NA_FLOAT_DEFAULT = -1000.
FILL_NA_OTHER_DEFAULT = ''
RENAME = {'long': 'lng'}  # long is a reserved keyword

# Kafka
BOOTSTRAP_SERVERS = "kafka:9092"
API_VERSION = (0, 10, 2)
TOPIC_TRUMP = "trump"
TOPIC_BIDEN = "biden"
PATH_TRUMP = os.environ['FILE_PATH_TRUMP']
PATH_BIDEN = os.environ['FILE_PATH_BIDEN']
ENCODER = 'utf-8'
