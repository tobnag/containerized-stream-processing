import numpy as np
import pandas as pd
from time import sleep
from json import dumps
from kafka import KafkaProducer

BOOTSTRAP_SERVERS = ['kafka:9092']
API_VERSION = (0, 10, 2)

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

def load_dataset(path, candidate):
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
    df.insert(1, 'candidate', candidate)
    return df

def load_datasets(path_trump, path_biden):
    print("Loading Trump's dataset...")
    df_trump = load_dataset(path=path_trump, candidate='Trump')
    print(f"Loaded Trump's dataset with {df_trump.size} rows.")
    print("Loading Biden's dataset...")
    df_biden = load_dataset(path=path_biden, candidate='Biden')
    print(f"Loaded Bidens's dataset with {df_biden.size} rows.")
    return df_trump, df_biden

def join_datasets(df_1, df_2):
    df = pd.concat([df_1, df_2], copy=False, ignore_index=True)
    df.sort_values('created_at', inplace=True, ignore_index=True)
    return df

def simulate_tweets(df, time_multiplicator=1, early_stopping=None):
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
                topic=data['candidate'].lower(),
                value=data.drop('candidate').to_json()
            )
        current_time = next_time
        sleep(wait_time)
    print("Tweet simulation is complete. This application exits now.")

if __name__ == '__main__':
    df_trump, df_biden = load_datasets(
        path_trump='/app/data/hashtag_donaldtrump.csv',
        path_biden='/app/data/hashtag_joebiden.csv'
    )
    df = join_datasets(df_trump, df_biden)
    kafka_server_healthcheck()
    simulate_tweets(df, time_multiplicator=1, early_stopping=60)