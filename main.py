import tweepy #bibliotēku importēšana
from tweepy import OAuthHandler
from textblob import TextBlob
import preprocessor as p
import statistics
from typing import Lists
from key_access import (consumer_key, consumer_secret, access_token, access_token_secret)


auth = OAuthHandler(consumer_key, consumer_secret) #autorizācija
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth) #tweet API test: rakstam tweet 
status = "Čau visiem, testēju Python API11#"
api.update_status(status)


def get_tweets(keyword: str) -> List[str]: # realtime tweet lejuplāde, strukturēšana
    all_tweets = [] #izvedam caur massivu ar List funkciju
    for tweet in tweepy.Cursor(api.search, q=keyword, tweet_mode= 'extended', since="2021-01-01", lang='lv').items(100): #nosacijumi ar cursor (vajadzīgs, lai varētu dabūt vairāk kritēriju)
        all_tweets.append(tweet.full_text) #norādam ka vajadzīgs vesels tweet tekts 
    return all_tweets #atgriežam rezultātu

def clean_tweets(all_tweets: List[str]) -> List[str]: #kritērijs, ko attīram un to strukturēšana
    tweets_clean = [] # izvadam kā massīvu caur List funkciju
    for tweet in all_tweets: #kritērijs ko vajadzējs paņemt
            tweets_clean.append(p.clean(tweet)) #tweet attīrīšana no masīviem elementiem ar preprocessor bibliotēku
    return tweets_clean #atgriežam tīru tekstu

def get_sentimet(all_tweets: List[str]) -> List[float]: #skaitam cik ir rindu (str to float)
    sentiment_scores = [] #veidojam tukšu massīvu, kur glabāsim rezultātu
    for tweet in all_tweets: #atkal kritērijs, ar ko operēsim
        blob = TextBlob(tweet) #definējam blob funkciju
        sentiment_scores.append(blob.sentiment.polarity) #nosakam sentiment funkcijas polaritāti priekš katra tweet ieraksta 
    return sentiment_scores #atgriežam rezultātus

def generate_average_sentiment_score(keyword: str) -> int: #izvadam atslēgvārdu ka veselu skaitli 
    tweets = get_tweets(keyword) #nosakam kodu secību
    tweets_clean = clean_tweets(tweets) #nosakam kodu secību
    sentiment_scores = get_sentimet(tweets_clean) # piesaistam (aprēķina) sentiment funkcijai cleaned tweet
    
    average_score = statistics.mean(sentiment_scores) #aprēķina vidējo vērtību caur statiskias funkciju

    return average_score #atrgriežam rezultātu pie lietotāja (man)


if __name__ == '__main__': #definējam galveno programmu
    print("Kas vairāk instresē tautai?") #jautājumu output
    first_thing = input() #ievadam pirmo keyword
    print("...vai...") #teksta izveide
    second_thing = input() #ievadam otro keyword
    print("\n") #definējam ka rakstam ar jauno līniju

    first_score = generate_average_sentiment_score(first_thing) #definējam pirmo vērtību
    second_score = generate_average_sentiment_score(second_thing) ##definējam otro vērtību

    if (first_score > second_score): #if funkcija
        print(f"Tautai instresē {first_thing} vairāk nekā {second_thing}!") #pirmā varianta rezultāts
    else: #nosakam pretējo variantu
        print(f"Tautai intresē {second_thing} vairāk nekā {first_thing}!") #otrā varianta rezultāts





