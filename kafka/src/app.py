import numpy as np
from time import sleep
from json import dumps
from kafka import KafkaProducer
from data import load_and_join_datasets
import conf

producer = KafkaProducer(
    bootstrap_servers=conf.BOOTSTRAP_SERVERS,
    api_version=conf.API_VERSION,
    value_serializer=lambda x: dumps(x, default=str).encode(conf.ENCODER)
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
    # slice the dataframe by time
    current_time = np.min(df[conf.COL_CREATED_AT])
    if early_stopping is None:
        end_time = np.max(df[conf.COL_CREATED_AT])
    else:
        end_time = current_time + np.timedelta64(early_stopping, 's')
    # wait_time is inversely proportional to the time multiplicator
    wait_time = 1. / time_multiplicator  # in seconds
    # send messages to kafka
    while current_time < end_time:
        next_time = current_time + np.timedelta64(1, 's')
        df_slice = df[(current_time<=df[conf.COL_CREATED_AT]) & (df[conf.COL_CREATED_AT]<next_time)]
        for _, row in df_slice.iterrows():
            topic = row[conf.COL_TOPIC]
            message = row.drop([conf.COL_TOPIC]).to_dict()
            producer.send(topic=topic, value=message)
        current_time = next_time
        sleep(wait_time)
    print("Tweet simulation is complete. This application exits now.")

def main():
    kafka_server_healthcheck()
    df = load_and_join_datasets()
    kafka_simulate_tweets(df, time_multiplicator=1, early_stopping=60)

if __name__ == '__main__':
    main()
