import datetime
import pandas as pd

from tweet import load_tweets, create_dataframe

class TweetProcessor():
    def __init__(self):
        prefilter_tweets = load_tweets('tweet_data/hydrated_tweets.json')
        tweets = []
        for k, tweet in enumerate(prefilter_tweets):
            if tweet.process_location() and k <= 100:
                tweet.tokenize_text()
                tweet.analyze_sentiment()
                tweets.append(tweet)
        self.ca_data, self.us_data = create_dataframe(tweets)

    def get_data(self, date: datetime.datetime) -> tuple[pd.DataFrame, pd.DataFrame, list[float], list[str]]:
        ca_rtn = self.ca_data

        us_rtn = self.us_data

        region_rtn = ca_rtn['location'].tolist() + us_rtn['location'].tolist()

        bins_rtn = [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1]

        return (ca_rtn, us_rtn, bins_rtn, region_rtn)
