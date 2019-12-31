# -*- coding: utf-8 -*-
"""
Created on Tue Jul  18 22:31:15 2019

@author: FARAZ AHMAD
"""
# General:
import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np      
from IPython.display import display
import matplotlib.pyplot as plt
countpos=countneg=countneut=0
#Get the Consumer Key and Access Token from Twitter Developers
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_SECRET = ""
#from credentials import *    
def twitter_setup():
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api
extractor = twitter_setup()

# We create a tweet list as follows:
tweets = extractor.user_timeline(screen_name="ANI", count=200)
print("Number of tweets extracted: {}.\n".format(len(tweets)))
print("5 recent tweets:\n")
for tweet in tweets[:5]:
    print()
data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

data['len']  = np.array([len(tweet.text) for tweet in tweets])
data['ID']   = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])
display(data.head(10))
print("starting visualisation...\n\n")
mean = np.mean(data['len'])

print("The lenght's average in tweets: {}".format(mean))
fav_max = np.max(data['Likes'])
rt_max  = np.max(data['RTs'])

fav = data[data.Likes == fav_max].index[0]
rt  = data[data.RTs == rt_max].index[0]

# Max FAVs:
print("The tweet with more likes is: \n{}".format(data['Tweets'][fav]))
print("Number of likes: {}".format(fav_max))
print("{} characters.\n".format(data['len'][fav]))

# Max RTs:
print("The tweet with more retweets is: \n{}".format(data['Tweets'][rt]))
print("Number of retweets: {}".format(rt_max))
print("{} characters.\n".format(data['len'][rt]))
tlen = pd.Series(data=data['len'].values, index=data['Date'])
tfav = pd.Series(data=data['Likes'].values, index=data['Date'])
tret = pd.Series(data=data['RTs'].values, index=data['Date'])
tlen.plot(figsize=(16,4), color='r');
tfav.plot(figsize=(16,4), label="Likes", legend=True)
tret.plot(figsize=(16,4), label="Retweets", legend=True); 
plt.show()

arr=[]
a1=[]
for tweet in tweets:
    tweeta = tweet.text
    tidy_tweet = (tweeta.strip().encode('ascii', 'ignore')).decode("utf-8") 
    #tidy_tweet=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", " ",tidy_tweet).split())
    #print(tidy_tweet)
    #print(cleanedTweet)
    analysis= TextBlob(tidy_tweet)
    #print (analysis.sentiment)
    if(analysis.sentiment.polarity > 0.2):
        polarity = 'Positive'
        countpos=countpos+1
        pol=1
    elif(0<=analysis.sentiment.polarity <=0.2):
        polarity = 'Neutral'
        countneut=countneut+1
        pol=0
    elif(analysis.sentiment.polarity < 0):
        polarity = 'Negative'
        countneg=countneg+1
        pol=-1
        
    #dic={}
    arr.append(polarity)
    a1.append(pol)
    #df=pd.DataFrame(arr)
    #data['Sentiment']=pd.Series(polarity)
    #dic['Tweet']=tidy_tweet
    #data.append(dic)
se=pd.Series(arr)
df=pd.DataFrame(data)
df['Sentiment']=se.values
ss=pd.Series(a1)
data['Senti']=ss.values
#print(df)

data.to_csv('recentnews.csv')
sources = []
for source in data['Source']:
    if source not in sources:
        sources.append(source)

# We print sources list:
print("Creation of content sources:")
for source in sources:
    print("* {}".format(source))


percent = np.zeros(len(sources))

for source in data['Source']:
    for index in range(len(sources)):
        if source == sources[index]:
            percent[index] += 1
            pass

#percent /= 100
print()
print("Positivity=",countpos/len(tweets)*100)
print("Negativity=", countneg/len(tweets)*100)
print("Neutral=", countneut/len(tweets)*100)

# Pie chart:
pie_chart = pd.Series(percent, index=sources, name='Sources')
pie_chart.plot.pie(fontsize=11, autopct='%.2f', figsize=(6, 6));
