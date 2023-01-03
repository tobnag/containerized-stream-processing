import pandas as pd

def load_dataframe(path, candidate):
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
    df.sort_values('created_at', inplace=True, ignore_index=True)
    df.insert(1, 'candidate', candidate)
    return df

def main():
    print("Loading Biden...")
    df_biden = load_dataframe(path='/app/data/hashtag_joebiden.csv', candidate='Biden')
    print("Loading Trump...")
    df_trump = load_dataframe(path='/app/data/hashtag_donaldtrump.csv', candidate='Trump')
    print(f"Biden: {df_biden.size}")
    print(f"Trump: {df_trump.size}")

def test():
    print("Module loaded!")

if __name__ == '__main__':
    main()
