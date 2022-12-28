import time
import pandas as pd

def main(path):
    df = pd.read_csv(path)
    print(f"Shape of CSV-file: {df.shape}")
    time.sleep(10)

def test():
    print("Module loaded!")

if __name__ == '__main__':
    main(path='/app/data/hashtag_joebiden.csv')
