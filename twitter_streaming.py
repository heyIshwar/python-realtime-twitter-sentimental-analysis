#Import the necessary methods from tweepy library
import tweepy
from dotenv import load_dotenv
from pathlib import Path
import os, re
from textblob import TextBlob
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")

positive, neutral, negative, total = 0, 0, 0, 0

# StreamListener class inherits from tweepy.StreamListener and overrides on_status/on_error methods.
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        global positive, neutral, negative, total
        total += 1
        tweet = status.text
        clean_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 

        analysis = TextBlob(clean_tweet)
        score = analysis.sentiment.polarity
        if score > 0:
            polarity = 'Positive'
            positive+=1
        elif score == 0:
            polarity = 'Neutral'
            neutral+=1
        else:
            polarity = 'Negative'
            negative+=1

        positive_percent = (positive/total)*100
        neutral_percent = (neutral/total)*100
        negative_percent = (negative/total)*100

        print('{:>5}'.format(total) + "\t" + status.id_str + "\t" + '{:>6}'.format('{:04.2f}'.format(score)) + "\t" + '{:<10}'.format(polarity) + "\t" + "| Total: " + '{:05.2f}'.format(positive_percent)+"% +ve  " + '{:05.2f}'.format(neutral_percent)+"% --  " + '{:05.2f}'.format(negative_percent) + "% -ve")

        # if "retweeted_status" attribute exists, flag this tweet as a retweet.
        is_retweet = hasattr(status, "retweeted_status")

        # check if text has been truncated
        if hasattr(status, "extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text

        # check if this is a quote tweet.
        is_quote = hasattr(status, "quoted_status")
        quoted_text = ""
        if is_quote:
            # check if quoted tweet's text has been truncated before recording it
            if hasattr(status.quoted_status, "extended_tweet"):
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text

        # remove characters that might cause problems with csv encoding
        remove_characters = [",", "\n"]
        for c in remove_characters:
            text.replace(c, " ")
            quoted_text.replace(c, " ")

        with open("out.csv", "a", encoding='utf-8') as f:
            f.write("%s,%s,%s,%s,%s,%s\n" % (status.created_at, status.user.screen_name, is_retweet, is_quote, text, quoted_text))

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()


if __name__ == "__main__":
    # complete authorization and initialize API endpoint
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # initialize stream
    streamListener = StreamListener()
    stream = tweepy.Stream( auth=api.auth, listener=streamListener, tweet_mode='extended')
    with open("out.csv", "w", encoding='utf-8') as f:
        f.write("date,user,is_retweet,is_quote,text,quoted_text\n")
    
    tags = ["#IndiaFightsCorona"]
    stream.filter(track=tags)
