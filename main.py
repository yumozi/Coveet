"""
The main program for the analyzer.
"""
from dataset import load_tweets


# ------------------------------------- Main ----------------------------------------

if __name__ == '__main__':
    tweets = load_tweets('data/hydrated_tweets.json')


