import pandas as pd
import conf

def _load_dataset(path, topic):
    df = pd.read_csv(path, dtype=conf.DTYPES, parse_dates=conf.PARSE_DATES,
                     lineterminator=conf.LINETERMINATOR)
    df.insert(1, conf.COL_TOPIC, topic)
    return df

def _load_datasets():
    # Load the first dataset
    print("Loading Trump's dataset...")
    df_trump = _load_dataset(path=conf.PATH_TRUMP, topic=conf.TOPIC_TRUMP)
    print(f"Loaded Trump's dataset with {df_trump.size} rows.")
    # Load the second dataset
    print("Loading Biden's dataset...")
    df_biden = _load_dataset(path=conf.PATH_BIDEN, topic=conf.TOPIC_BIDEN)
    print(f"Loaded Bidens's dataset with {df_biden.size} rows.")
    dfs = [df_trump, df_biden]
    return dfs

def _join_datasets(dfs):
    df = pd.concat(dfs, copy=False, ignore_index=True)
    df.sort_values(conf.COL_CREATED_AT, inplace=True, ignore_index=True)
    return df

def load_and_join_datasets():
    dfs = _load_datasets()
    df = _join_datasets(dfs)
    return df

def clean_dataset(df):
    # Basic cleaning
    df.dropna(subset=conf.DROP_NA, inplace=True)
    df.drop_duplicates(subset=conf.DROP_DUPLICATES, inplace=True)
    df.sort_values(conf.COL_CREATED_AT, ignore_index=True, inplace=True)

    # Handle missing values
    df[conf.FILL_NA_INT] = df[conf.FILL_NA_INT].fillna(conf.FILL_NA_INT_DEFAULT)
    df[conf.FILL_NA_FLOAT] = df[conf.FILL_NA_FLOAT].fillna(conf.FILL_NA_FLOAT_DEFAULT)
    df.fillna(conf.FILL_NA_OTHER_DEFAULT, inplace=True)

    # Rename columns to avoid reserved keywords
    df.rename(columns=conf.RENAME, inplace=True)
    return df
