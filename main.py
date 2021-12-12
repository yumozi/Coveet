"""
The main program for the analyzer.
"""
from tweet import load_tweets
import argparse
from gui import display_map
import sys


# ————————————————————————————————— Argparse —————————————————————————————————
def parse_args():
    """Parse the command line arguments.
    """
    parser = argparse.ArgumentParser(description="Argparse for Interactive Map")
    parser.add_argument("--mode",
                        dest="mode",
                        help="The mode of the map: covid/sentiment/comparison",
                        default='comparison',
                        type=str)
    args = parser.parse_args()

    if args.mode not in {'covid', 'sentiment', 'comparison'}:
        raise ValueError("Aborting: Invalid Mode.")
    elif args.mode == 'covid':
        print("Mode: Covid Map.")
    elif args.mode == 'sentiment':
        print("Mode: Sentiment Map.")
    else:
        print("Mode: Comparison Map.")

    return args


# ————————————————————————————————— Main —————————————————————————————————
if __name__ == '__main__':
    args = parse_args()

    print("Loading Tweets...")
    prefilter_tweets = load_tweets('data/hydrated_tweets.json')

    print("Processing Tweets...")
    tweets = []
    for tweet in prefilter_tweets:
        if tweet.process_location():
            tweet.tokenize_text()
            tweet.analyze_sentiment()
            tweets.append(tweet)

    print("Displaying map...")
    display_map(args.mode)


