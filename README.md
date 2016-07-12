#twitter-streaming-api

1. About
2. Requirements
3. Twitter Access
4. The Code
5. Fonts

## About

This is a python program to get tweets in streaming from twitter database and return in a json.

## Requirements

1. Python 3.0 installed.
2. Install Tweepy: ```pip install tweepy```
3. Twitter Account.

## Twitter Access

To get twitter data, you need 4 access key. Its very simple to get those.

Go to https://apps.twitter.com and click in 'Create New App' and insert the request informations.

Now you create a Twitter App, lets go get there keys. Open the App page and click in Keys and Access Token.

Alright, now we knows the App Key and the App Token.

## The Code

```
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains yours credentials to access Twitter API 
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter tweets from the words.
    stream.filter(track=['key1', 'key2'])
```

## Fonts

Tweepy GitHub: https://github.com/tweepy/tweepy

This code were based from this link: http://adilmoujahid.com/posts/2014/07/twitter-analytics/