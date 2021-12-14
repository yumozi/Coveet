import json
from country_provinces import country_provinces
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from statistics import mean
import pandas as pd
import datetime


class Tweet:
    """A tweet and its related information

    Instance Attributes:
        - text: The text of the tweet
        - tokenized_text: The tokenized text of the tweet
        - location: The location of the user who posted the tweet
        - country: The country of the user who posted the tweet
        - score: The sentiment score of the tweet
    """
    _text: str
    _tokenized_text: list
    _location: str
    _country: str
    _score: float

    def __init__(self, text, location) -> None:
        self._text = text
        self._tokenized_text = []
        self._location = location
        self._country = ''
        self._score = 0.0
        self.tokenize_text()
        self.analyze_sentiment()

    def tokenize_text(self) -> None:
        """Tokenizes the text of the tweet"""
        self._tokenized_text = nltk.sent_tokenize(self._text)

    def analyze_sentiment(self) -> None:
        """Sets average sentiment of a tweet from its tokenized text"""
        sia = SentimentIntensityAnalyzer()
        scores = [sia.polarity_scores(s)["compound"] for s in self._tokenized_text]
        self._score = mean(scores)

    def process_location(self) -> bool:
        """Set the user_location attribute to the state/province of the user
        Return whether this was successful"""

        tokenized_location = self._location.split(' ')
        for word in tokenized_location:
            if word.lower() in country_provinces['Canada'] or word.lower() in country_provinces['United States']:
                self._location = word.lower()
                self._country = 'Canada' if word.lower() in country_provinces['Canada'] else 'United States'
                return True
        return False

    def get_location(self) -> str:
        """Returns the location of the tweet"""
        return self._location

    def get_score(self) -> float:
        """Returns the sentiment score of the tweet"""
        return self._score

    def get_country(self) -> str:
        """Returns the country of the tweet"""
        return self._country

    def __str__(self) -> str:
        """Returns the first 100 characters of the tweet"""
        return self._text[:100] + '...'


def get_tweets(date: datetime.datetime) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns the average tweet sentiment for every region and the maximum for all the regions, given a date
    The resulting tuple holds the american data at index 0 and the canadian data at index 1.

    Preconditions:
      - date in self.possible_dates
    """
    path = "data\\" + date.strftime('%Y-%m-%d') + "\\hydrated_tweets.json"

    prefilter_tweets = load_tweets(path)
    tweets = []
    for tweet in prefilter_tweets:
        if tweet.process_location():
            tweets.append(tweet)
    ca_data, us_data = create_dataframe(tweets)

    return ca_data, us_data


def load_tweets(filename: str) -> list:
    """Loads a list of tweets with valid user location from a json file
    """
    json_tweets = []
    tweets = []

    with open(filename) as f:
        for json_tweet in f:
            json_tweet = json.loads(json_tweet)
            if json_tweet['user']['location'] != "":
                json_tweets.append(json_tweet)

    for json_tweet in json_tweets:
        tweets.append(Tweet(json_tweet['text'], json_tweet['user']['location']))

    return tweets


def create_dataframe(tweets: list) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Creates a pandas dataframe from a list of tweets with columns: location, sentiment score
    """
    canada_scores = {}
    us_scores = {}
    for tweet in tweets:
        location = tweet.get_location()
        if tweet.get_country() == 'Canada':
            if location not in canada_scores:
                canada_scores[location] = []
            canada_scores[location].append(tweet.get_score())
        else:
            if location not in us_scores:
                us_scores[location] = []
            us_scores[location].append(tweet.get_score())

    for location in canada_scores:
        canada_scores[location] = sum(canada_scores[location]) / len(canada_scores[location])
    for location in us_scores:
        us_scores[location] = sum(us_scores[location]) / len(us_scores[location])

    canada_dataframe = {'location': [], 'value': []}
    us_dataframe = {'location': [], 'value': []}
    for location in canada_scores:
        canada_dataframe['location'].append(location.title())
        canada_dataframe['value'].append(canada_scores[location])
    for location in us_scores:
        us_dataframe['location'].append(location.title())
        us_dataframe['value'].append(us_scores[location])

    return pd.DataFrame.from_dict(canada_dataframe), pd.DataFrame.from_dict(us_dataframe)
