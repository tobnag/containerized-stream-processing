import os
import logging

logging.basicConfig(level=logging.INFO)

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
RENAME = {'long': 'lon'}  # long is a reserved keyword

# Kafka
BOOTSTRAP_SERVERS = "kafka:9092"
API_VERSION = (0, 10, 2)
TOPIC_TRUMP = "trump"
TOPIC_BIDEN = "biden"
PATH_TRUMP = os.path.join(os.environ['CONTAINER_DATA_FOLDER'], os.environ['FILE_NAME_TRUMP'])
PATH_BIDEN = os.path.join(os.environ['CONTAINER_DATA_FOLDER'], os.environ['FILE_NAME_BIDEN'])
ENCODER = 'utf-8'

# App configuration
TIME_MULTIPLIER = float(os.environ['TIME_MULTIPLIER'])
if TIME_MULTIPLIER < 1:
    logging.warning(f"TIME_MULTIPLIER={TIME_MULTIPLIER} must be >= 1. Setting it to 1.")
    TIME_MULTIPLIER = 1
elif TIME_MULTIPLIER > 100:
    logging.warning(f"TIME_MULTIPLIER={TIME_MULTIPLIER} must be <= 100. Setting it to 100.")
    TIME_MULTIPLIER = 100
