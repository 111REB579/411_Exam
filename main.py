import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import preprocessor as p
import statistics
from typing import Lists
from key_access import (consumer_key, consumer_secret, access_token, access_token_secret)


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
status = "Čau visiem, testēju Python API11#"
api.update_status(status)


def get_tweets(keyword: str) -> List[str]:
    all_tweets = []
    for tweet in tweepy.Cursor(api.search, q=keyword, tweet_mode= 'extended', since="2021-01-01", lang='lv').items(100):
        all_tweets.append(tweet.full_text)
    return all_tweets

def clean_tweets(all_tweets: List[str]) -> List[str]:
    tweets_clean = []
    for tweet in all_tweets:
            tweets_clean.append(p.clean(tweet))
    return tweets_clean

def get_sentimet(all_tweets: List[str]) -> List[float]:
    sentiment_scores = []
    for tweet in all_tweets:
        blob = TextBlob(tweet)
        sentiment_scores.append(blob.sentiment.polarity)
    return sentiment_scores

def generate_average_sentiment_score(keyword: str) -> int:
    tweets = get_tweets(keyword)
    tweets_clean = clean_tweets(tweets)
    sentiment_scores = get_sentimet(tweets_clean)

    average_score = statistics.mean(sentiment_scores)

    return average_score


if __name__ == '__main__':
    print("Kas vairāk instresē tautai?")
    first_thing = input()
    print("...vai...")
    second_thing = input()
    print("\n")

    first_score = generate_average_sentiment_score(first_thing)
    second_score = generate_average_sentiment_score(second_thing)

    if (first_score > second_score):
        print(f"Tautai instresē {first_thing} vairāk nekā {second_thing}!")
    else:
        print(f"Tautai intresē {second_thing} vairāk nekā {first_thing}!")





