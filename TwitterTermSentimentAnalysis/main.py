from textblob import TextBlob
import tweepy
import sys

api_key = ''
api_key_secret = ''
access_token = ''
access_token_secret = ''

auth_handler = tweepy.OAuthHandler(consumer_key=api_key, consumer_secret=api_key_secret)
auth_handler.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler)

search_term = 'bitcoin'
tweet_amount = 200
polarity = 0


tweets = tweepy.Cursor(api.search_tweets, q=search_term, lang='en').items(tweet_amount)

for tweet in tweets:
    final_text = tweet.text.replace('RT', '')
    if final_text.startswith(' @'):
        position = final_text.index(':')
        final_text = final_text[position+2:]
    if final_text.startswith('@'):
        position = final_text.index(' ')
        final_text = final_text[position+2:]
    analysis = TextBlob(final_text)
    polarity += analysis.polarity

print(polarity)
