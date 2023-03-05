import pandas as pd
import const

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

def load_datasets(path_trump=const.PATH_TRUMP, path_biden=const.PATH_BIDEN):
    print("Loading Trump's dataset...")
    df_trump = load_dataset(path=path_trump, topic=const.TOPIC_TRUMP)
    print(f"Loaded Trump's dataset with {df_trump.size} rows.")
    print("Loading Biden's dataset...")
    df_biden = load_dataset(path=path_biden, topic=const.TOPIC_BIDEN)
    print(f"Loaded Bidens's dataset with {df_biden.size} rows.")
    return df_trump, df_biden

def join_datasets(df_1, df_2):
    df = pd.concat([df_1, df_2], copy=False, ignore_index=True)
    df.sort_values('created_at', inplace=True, ignore_index=True)
    return df
