
# coding: utf-8

# In[8]:

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json

from nltk.sentiment.util import demo_liu_hu_lexicon


#consumer key, consumer secret, access token, access secret.
ckey="zD5nLXaLzYmp4IUDiI8rdM7by"
csecret="hJmVNtViHRXxmLeERO9dww9zlGct6a1DjznMhBLbuOY9BV6JYQ"
atoken="837081907099811840-JiRiAbpBMQHMtrrwczfGBqzutYjbCPL"
asecret="CXXobZSKEz02osSVaodVEmmuI3Iq6dHQbU6Q8x0Yzsq5h"

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        
        tweet = all_data["text"]
        
        username = all_data["user"]["screen_name"]
        sentiment = demo_liu_hu_lexicon(tweet)
        
        print(tweet, sentiment)
        
        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["amazon", "comcast"])

