"""Coveet: Twitter COVID Sentiment Analyser

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Eric Xue and Jeremy Liu.
"""
import argparse
from gui import display_map


# ————————————————————————————————— Argparse —————————————————————————————————
def parse_args() -> argparse.Namespace:
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

    print("Displaying map...")
    display_map(args.mode)
