import json
from country_provinces import country_provinces
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from statistics import mean

class Tweet:
    """A tweet and its related information

    Instance Attributes:
        - text: The text of the tweet
        - tokenized_text: The tokenized text of the tweet
        - user_location: The location of the user who posted the tweet
        - average_sentiment: The average sentiment of the tweet
    """
    _text: str
    _tokenized_text: list
    _user_location: str
    _average_sentiment: float

    def __init__(self, text, user_location):
        self._text = text
        self._tokenized_text = []
        self._user_location = user_location
        self._average_sentiment = 0.0

    def tokenize_text(self):
        """Tokenizes the text of the tweet"""
        self._tokenized_text = nltk.sent_tokenize(self._text)

    def analyze_sentiment(self):
        """Sets average sentiment of a tweet from its tokenized text"""
        sia = SentimentIntensityAnalyzer()
        scores = [sia.polarity_scores(s)["compound"] for s in self._tokenized_text]
        self._average_sentiment = mean(scores)

    def process_location(self) -> bool:
        """Set the user_location attribute to the state/province of the user
        Return whether this was successful"""

        tokenized_location = self._user_location.split(' ')
        for word in tokenized_location:
            if word.lower() in country_provinces['Canada'] or word.lower() in country_provinces['United States']:
                self._user_location = word.lower()
                return True
        return False

    def __str__(self):
        """Returns the first 100 characters of the tweet"""
        return self._text[:100] + '...'


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





