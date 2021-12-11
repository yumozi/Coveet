"""
The main program for the analyzer.
"""
from tweet import load_tweets
import argparse
import pdb


# ————————————————————————————————— Argparse —————————————————————————————————
def parse_args():
    """Parse the command line arguments.
    """
    parser = argparse.ArgumentParser(description="Argparse for Interactive Map")
    parser.add_argument("--is_comparison",
                        dest="is_comparison",
                        help="Whether or not to run a comparison on the region",
                        default=False,
                        type=bool)
    args = parser.parse_args()

    if args.is_comparison:
        print("Displaying Sentiment vs Covid Cases Map...")
    else:
        print("Displaying Sentiment Map...")

    return args


# ————————————————————————————————— Main —————————————————————————————————
if __name__ == '__main__':
    args = parse_args()
    prefilter_tweets = load_tweets('data/hydrated_tweets.json')
    tweets = []
    for tweet in prefilter_tweets:
        if tweet.process_location():
            tweet.tokenize_text()
            tweet.analyze_sentiment()
            tweets.append(tweet)



