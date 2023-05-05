import numpy as np
from time import sleep
from json import dumps
from kafka import KafkaProducer
from data import load_and_join_datasets, clean_dataset
import conf
import logging
import time

producer = KafkaProducer(
    bootstrap_servers=conf.BOOTSTRAP_SERVERS,
    api_version=conf.API_VERSION,
    value_serializer=lambda x: dumps(x, default=str).encode(conf.ENCODER)
)

def kafka_server_healthcheck(max_wait_time_seconds=30):
    i = 0
    while i < max_wait_time_seconds:
        if producer.bootstrap_connected():
            logging.info("Healthcheck successful. Kafka bootstrap server is connected.")
            return
        else:
            logging.info("Healthchek not successful. Kafka bootstrap server is not connected. Pause and retry.")
            sleep(1)
            i += 1
    error_message = f"Timeout: Connection to Kafka server could not be established after {max_wait_time_seconds} seconds."
    logging.error(error_message)
    raise RuntimeError(error_message)

def kafka_simulate_tweets(df):
    logging.info("Started tweet simulation. This application will exit when the simulation is complete.")
    # slice the dataframe by time
    current_time = np.min(df[conf.COL_CREATED_AT])
    end_time = np.max(df[conf.COL_CREATED_AT])
    # wait_time is inversely proportional to the time multiplicator
    wait_time = 1. / conf.TIME_MULTIPLIER  # in seconds
    # send messages to kafka
    while current_time < end_time:
        ts_start = time.time_ns()  # code execution time
        next_time = current_time + np.timedelta64(1, 's')
        df_slice = df[(current_time<=df[conf.COL_CREATED_AT]) & (df[conf.COL_CREATED_AT]<next_time)]
        for _, row in df_slice.iterrows():
            topic = row[conf.COL_TOPIC]
            message = row.drop([conf.COL_TOPIC]).to_dict()
            producer.send(topic=topic, value=message)
        current_time = next_time
        ts_end = time.time_ns()  # code execution time
        # compute the time to sleep until the next iteration
        sleep_time = max(0, wait_time - (ts_end - ts_start) / 1e9)
        sleep(sleep_time)
    logging.info("Tweet simulation is complete. This application exits now.")

def main():
    df = load_and_join_datasets()
    df = clean_dataset(df)
    kafka_server_healthcheck()
    kafka_simulate_tweets(df)

if __name__ == '__main__':
    main()
