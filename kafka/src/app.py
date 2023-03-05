import numpy as np
from time import sleep
from json import dumps
from kafka import KafkaProducer
from data import load_datasets, join_datasets
import const

producer = KafkaProducer(
    bootstrap_servers=const.BOOTSTRAP_SERVERS,
    api_version=const.API_VERSION,
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

def main():
    df_trump, df_biden = load_datasets()
    df = join_datasets(df_trump, df_biden)
    kafka_server_healthcheck()
    kafka_simulate_tweets(df, time_multiplicator=1, early_stopping=60)

if __name__ == '__main__':
    main()
