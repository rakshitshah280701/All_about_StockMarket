from cgitb import text
from statistics import mode
import tweepy
import configparser
import pandas as pd
from textblob import TextBlob
#import matplotlib.pyplot as plt
import plotly.graph_objects as go

# config = configparser.ConfigParser()
# config.read('config.ini')

# api_key = config['twitter']['api_key']
# api_key_secret = config['twitter']['api_key_secret']
# acces_token = config['twitter']['access_token']
# acces_token_secret = config['twitter']['access_token_secret']

api_key = "xUh5fETyehGTSrNeETY0LaCSG"
api_key_secret = "ZqEK42bAfKfAsATvDF7u54fci31SREZWBDR9BGI1GddI99U2DF"
access_token = "1492571731403640832-9gsDqrMrh0t1Pds4F3ILHQilpacqDZ"
access_secret = "jwXHCFL1rVFxlQVmMPe9EhgFAk0J6m7wfjfPUtSJbzTao"

#print(api_key)
auth = tweepy.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_secret)

api = tweepy.API(auth)
#public_tweets = api.home_timeline()
choice= input("Enter the Hashtag:")
tweets=tweepy.Cursor(api.search_tweets,q=choice).items(50)
#print(public_tweets[0].user.screen_name,public_tweets[0].text)

bullish=0
bearish=0
consolidation=0

colums = ['Time','User','Tweet']
data = []
for tweet in tweets:
    data.append([tweet.created_at,tweet.user.screen_name,tweet.text])
    sentiment=TextBlob(tweet.text)
    if (sentiment.sentiment.polarity==0):
        consolidation=consolidation+1
    
    elif (sentiment.sentiment.polarity>0):
        bullish=bullish+1

    elif (sentiment.sentiment.polarity<0):
        bearish=bearish+1

# sizes=[bullish,bearish,consolidation]
# labels='Bullish','Bearish','Consolidation'
# colors=['gold', 'yellowgreen', 'lightcoral']
# plt.pie(sizes, explode=None, labels=labels, colors=colors,autopct='%1.1f%%', startangle=140)
# plt.axis('equal')
# fig1 = plt.gcf()
# #plt.show()
# plt.draw
# fig1.savefig('R:\sem6-mini-project\static\myplot.png',dpi=100)

# if (bullish>bearish) and (bullish>consolidation):
#     largest=bullish
# elif (bearish>bullish) and (bearish>consolidation):
#     largest=bearish
# else:
#     largest=consolidation
# print("largest is : ",largest)
total=bullish+bearish+consolidation
bullish_percentage= (bullish/total)*100
bearish_percentage= (bearish/total)*100
consolidation_percentage= (consolidation/total)*100
fig = go.Figure(go.Indicator(
    domain = {'x':[0,1],'y':[0,1]},
    value = bullish_percentage,
    mode = 'gauge+number',
    title = {'text': "Bullish Sentiment"},
    gauge = {'axis':{'range': [None,100]}}
))
# fig.savefig('R:\sem6-mini-project\static\myplot.png',dpi=100)
#fig.show()
fig.write_image("static/sentiment1.png")

fig1 = go.Figure(go.Indicator(
    domain = {'x':[0,1],'y':[0,1]},
    value = bearish_percentage,
    mode = 'gauge+number',
    title = {'text': "Bearish Sentiment"},
    gauge = {'axis':{'range': [None,100]}}
))
# fig.savefig('R:\sem6-mini-project\static\myplot.png',dpi=100)
#fig.show()
fig1.write_image("static/sentiment2.png")

fig2 = go.Figure(go.Indicator(
    domain = {'x':[0,1],'y':[0,1]},
    value = consolidation_percentage,
    mode = 'gauge+number',
    title = {'text': "Consolidation Sentiment"},
    gauge = {'axis':{'range': [None,100]}}
))
# fig.savefig('R:\sem6-mini-project\static\myplot.png',dpi=100)
#fig.show()
fig2.write_image("static/sentiment3.png")



df = pd.DataFrame(data, columns=colums)
#print(df)
#df.to_csv('C:')
print(bullish,"Bullish")
print(bearish,"Bearish")
print(consolidation,"consolidation")
