import datetime
import pandas as pd
import os
from tweet import load_tweets, create_dataframe
import tweet

class TweetProcessor():
    def __init__(self):
        # Cache the currently logged dates in the folder
        self.possible_dates = [x for x in os.listdir(os.getcwd() + "\\" + "data")]

        path = "data\\" + self.possible_dates[0] + "\\hydrated_tweets.json"


    def get_data(self, date: datetime.datetime) -> tuple[pd.DataFrame, pd.DataFrame, list[float], list[str]]:
        date_str = date.strftime('%Y-%m-%d')  # Convert our datetime into (year month day) format
        if date_str in self.possible_dates:
            path = "data\\" + date_str + "\\hydrated_tweets.json"
            prefilter_tweets = load_tweets(path)
            tweets = []
            for k, tweet in enumerate(prefilter_tweets):
                if tweet.process_location():
                    tweet.tokenize_text()
                    tweet.analyze_sentiment()
                    tweets.append(tweet)
            self.ca_data, self.us_data = create_dataframe(tweets)
        else:
            self.ca_data, self.us_data = create_dataframe([])

        ca_rtn = self.ca_data
        us_rtn = self.us_data

        region_rtn = ca_rtn['location'].tolist() + us_rtn['location'].tolist()

        bins_rtn = [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1]

        return (ca_rtn, us_rtn, bins_rtn, region_rtn)

    def get_tweets(self, path) -> list[tweet]:
        """Returns parsed tweets, loaded from a file, given its path"""
        prefilter_tweets = load_tweets(path)
        tweets = []
        for _tweet in prefilter_tweets:
            if _tweet.process_location():
                _tweet.tokenize_text()
                _tweet.analyze_sentiment()
                tweets.append(_tweet)
        return tweets

if __name__ == "__main__":
    a = TweetProcessor()
    data = a.get_data(datetime.datetime(2020, 8, 1))
    print(data[0].shape, data[1].shape, data[2], data[3])
