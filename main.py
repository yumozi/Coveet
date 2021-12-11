"""
The main program for the analyzer.
"""
from dataset import load_tweets
import argparse


# ————————————————————————————————— Argparse —————————————————————————————————
def parse_args():
    """Parse the command line arguments.
    """
    parser = argparse.ArgumentParser(description="Interactive menu for ")
    parser.add_argument("region", type=str, help="Region to analyse")
    parser.add_argument("-is_comparison", help="Whether or not to run a comparison on the region", action="store_true")
    args = parser.parse_args()

    if args.region:
        # If a region is selected
        print("Region Selected: {}".format(args.region))
        if args.is_comparison:
            # If the comparison flag is raised
            print("Comparison Selected")
        else:
            # Otherwise
            print("Normal Map")
    else:
        # If no region specified
        print("No region specified")
    return args


# ————————————————————————————————— Main —————————————————————————————————
if __name__ == '__main__':
    args = parse_args()
    tweets = load_tweets('data/hydrated_tweets.json')


