import os
import numpy as np
import pandas as pd
from time import sleep
from json import dumps
from kafka import KafkaProducer

BOOTSTRAP_SERVERS = f"{os.environ['KAFKA_ADVERTISED_HOST_NAME']}:{os.environ['KAFKA_PORT']}"
API_VERSION = tuple(map(lambda s: int(s.strip()), os.environ['KAFKA_API_VERSION'].split(',')))
TOPIC_TRUMP = os.environ['KAFKA_TOPIC_TRUMP']
TOPIC_BIDEN = os.environ['KAFKA_TOPIC_BIDEN']
PATH_TRUMP = os.environ['FILE_PATH_TRUMP']
PATH_BIDEN = os.environ['FILE_PATH_BIDEN']

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    api_version=API_VERSION,
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

def kafka_server_healthcheck(max_wait_time_seconds=10):
    i = 0
    while i < max_wait_time_seconds:
        if producer.bootstrap_connected():
            print("Healthcheck successful. Kafka bootstrap server is connected.")
            return
        else:
            print("Kafka bootstrap server is not connected. Pause and retry.")
            sleep(1)
            i += 1
    raise RuntimeError(
        f"Timeout: Connection to Kafka server could not be established after {max_wait_time_seconds} seconds.")

def load_dataset(path, topic):
    dtype = {
        'tweet_id': int,
        'likes': int,
        'retweet_count': int,
        'user_id': int,
        'user_followers_count': int,
        'lat': float,
        'long': float
    }
    parse_dates = ['created_at', 'collected_at']
    df = pd.read_csv(path, dtype=dtype, parse_dates=parse_dates, lineterminator='\n')
    df.drop_duplicates(subset=['created_at', 'tweet_id', 'user_id'], inplace=True)
    df.sort_values('created_at', ignore_index=True, inplace=True)
    df.insert(1, 'topic', topic)
    return df

def load_datasets(path_trump=PATH_TRUMP, path_biden=PATH_BIDEN):
    print("Loading Trump's dataset...")
    df_trump = load_dataset(path=path_trump, topic=TOPIC_TRUMP)
    print(f"Loaded Trump's dataset with {df_trump.size} rows.")
    print("Loading Biden's dataset...")
    df_biden = load_dataset(path=path_biden, topic=TOPIC_BIDEN)
    print(f"Loaded Bidens's dataset with {df_biden.size} rows.")
    return df_trump, df_biden

def join_datasets(df_1, df_2):
    df = pd.concat([df_1, df_2], copy=False, ignore_index=True)
    df.sort_values('created_at', inplace=True, ignore_index=True)
    return df

def kafka_simulate_tweets(df, time_multiplicator=1, early_stopping=None):
    print("Started tweet simulation. This application will exit when the simulation is complete.")
    t = 'created_at'
    current_time = np.min(df[t])
    if early_stopping is None:
        end_time = np.max(df[t])
    else:
        end_time = current_time + np.timedelta64(early_stopping, 's')
    wait_time = 1. / time_multiplicator  # in seconds
    while current_time < end_time:
        next_time = current_time + np.timedelta64(1, 's')
        df_slice = df[np.logical_and(current_time<=df[t], df[t]<next_time)]
        for _, data in df_slice.iterrows():
            producer.send(
                topic=data['topic'],
                value=data.drop('topic').to_json()
            )
        current_time = next_time
        sleep(wait_time)
    print("Tweet simulation is complete. This application exits now.")

if __name__ == '__main__':
    df_trump, df_biden = load_datasets()
    df = join_datasets(df_trump, df_biden)
    kafka_server_healthcheck()
    kafka_simulate_tweets(df, time_multiplicator=1, early_stopping=60)