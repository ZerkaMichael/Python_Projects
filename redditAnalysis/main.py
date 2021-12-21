import praw
from data import *
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#Variables
posts = 0
count = 0
c_analyzed = 0
tickers = {}
titles = []
a_comments =  {}
cmt_auth = {}
times = []
top = []
scores = {}
s = {}


#Parameters
subs = ['wallstreetbets' ]
post_flairs = {'Daily Discussion', 'Weekend Discussion', 'Discussion'}
goodAuth = {'AutoModerator'}
uniqueCmt = True
ignoreAuth = {'example'}
upvoteRatio = 0.70
ups = 20
limit = 1
upvotes = 2
picks = 10
picksToAnalyze = 5

#Reddit Login
reddit = praw.Reddit(user_agent="Comment Extraction",
    client_id="sRUpaKaosxzQAg",
    client_secret="WTQl_UKpctLF9PISo2C-FnKQ721ohQ",
    username="ryder_Bot",
    password="Zxcvbnm123!123!")

#Find viable comments, count tickers, and add to list
for sub in subs:
    subreddit = reddit.subreddit(sub)
    hot_sort = subreddit.hot()
    #Extracting comments
    for submission in hot_sort:
        flair = submission.link_flair_text
        author = submission.author.name
        #Check Parameters
        if submission.upvote_ratio >= upvoteRatio and submission.ups > ups and (flair in post_flairs or flair is None) and author not in ignoreAuth:
            submission.comment_sort = 'new'
            comments = submission.comments
            titles.append(submission.title)
            posts += 1
            try:
                submission.comments.replace_more(limit=limit)
                for comment in comments:
                    #Pass deleted accounts
                    try: auth = comment.author.name
                    except: pass
                    c_analyzed += 1
                    #Check Parameters
                    if comment.score > upvotes and auth not in ignoreAuth:
                        split = comment.body.split(" ")
                        for word in split:
                            word = word.replace("$", "")
                            # upper = ticker, length of ticker <= 5, excluded words,
                            if word.isupper() and len(word) <= 5 and word not in blacklist and word in us:
                                #Unique check
                                if uniqueCmt and auth not in goodAuth:
                                    try:
                                        if auth in cmt_auth[word]: break
                                    except: pass
                                #Count stock tickers
                                if word in tickers:
                                    tickers[word] += 1
                                    a_comments[word].append(comment.body)
                                    cmt_auth[word].append(auth)
                                    count += 1
                                else:
                                    tickers[word] = 1
                                    cmt_auth[word] = [auth]
                                    a_comments[word] = [comment.body]
                                    count += 1
            #print error on exception
            except Exception as e: print(e)



#Sort
symbols = dict(sorted(tickers.items(), key=lambda item: item[1], reverse = True))
top_picks = list(symbols.keys())[0:picks]

#Print stats
print("{c} comments in {p} posts in {s} subreddits.\n".format(c=c_analyzed, p=posts, s=len(subs)))

#Count and print
for i in top_picks:
    print(f"{i}: {symbols[i]}")
    times.append(symbols[i])
    top.append(f"{i}: {symbols[i]}")

#Sentiment analysis
vader = SentimentIntensityAnalyzer()
#Add weighted words
vader.lexicon.update(weighted_words)
picks_sentiment = list(symbols.keys())[0:picksToAnalyze]

#Run sentiment analysis
for symbol in picks_sentiment:
    stock_comments = a_comments[symbol]
    for cmnt in stock_comments:
        score = vader.polarity_scores(cmnt)
        if symbol in s:
            s[symbol][cmnt] = score
        else:
            s[symbol] = {cmnt:score}
        if symbol in scores:
            for key, _ in score.items():
                scores[symbol][key] += score[key]
        else:
            scores[symbol] = score

    #Find average
    for key in score:
        scores[symbol][key] = scores[symbol][key] / symbols[symbol]
        scores[symbol][key]  = "{pol:.3f}".format(pol=scores[symbol][key])

#Print
print("\n\nSentiment analysis")
df = pd.DataFrame(scores)
df.index = ['Bearish', 'Neutral', 'Bullish', 'Total/Compound']
df = df.T
print(df)
