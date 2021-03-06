import json
import tweepy
import boto3
import bybit

ssm = boto3.client('ssm', region_name="us-east-1")
comprehend = boto3.client('comprehend', region_name="us-east-1")

try:
    api_key = ssm.get_parameter(Name='elongate_api_key')['Parameter']['Value']
    api_secret_key = ssm.get_parameter(Name='elongate_api_secret_key')['Parameter']['Value']
    access_token = ssm.get_parameter(Name='elongate_access_token')['Parameter']['Value']
    access_token_secret = ssm.get_parameter(Name='elongate_access_token_secret')['Parameter']['Value']
    bybit_api_secret = ssm.get_parameter(Name='elongate_bybit_api_secret')['Parameter']['Value']
    bybit_secret = ssm.get_parameter(Name='elongate_bybit_secret')['Parameter']['Value']
except Exception as e:
    print(f"failed to get API keys from SSM :: {e}")

try:
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    bybit_client  = bybit.bybit(api_key=bybit_secret, api_secret=bybit_api_secret)
except Exception as e:
    print(f"failed to connect to 3rd Party API :: {e}")

def get_bybit_link():
    try:
        print("testing bybit client...")
        print(bybit_client)
    except Exception as e:
        print(e)
    return "coming soon"

def check_recent_elon_tweets(event, _):
    print(event)
    recent_tweet_sentiment = {}
    for tweet in api.user_timeline("elonmusk"):
        print(tweet)
        url = f"https://twitter.com/elonmusk/status/{tweet.id}"
        try:
            recent_tweet_sentiment[url] = comprehend.detect_sentiment(Text=(tweet.text),LanguageCode='en')['Sentiment']
        except Exception as e:
            print(e)
            return {
                "statusCode": 555,
                "headers": {
                    'Access-Control-Allow-Origin': '*',
                },
                "body": json.dumps({"error": e})
            }
    return {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Origin': '*',
        },
        "body": json.dumps(recent_tweet_sentiment)
    }
def notify_result(event, _):
    return {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Origin': '*',
        },
        "body": json.dumps({"coming soon": "coming_soon"})
    }

def analyze_tweet(event, _):
    print(event)
    try:
        post_data = json.loads(event['body'])
        if '?' in post_data['tweet']:
            tweet_url = post_data['tweet'].split('?')[0]                # remove ? from tweet
        else:
            tweet_url = post_data['tweet']
        tweet_id = tweet_url.split('/')[-1]
        
        elon_tweet = api.get_status(tweet_id)
        print(f"found elon tweet :: {elon_tweet}")
        #regex elon tweet link
        #check if tweet is live
        #check if tweet mentions stonk/coin
        elon_tweet_text = elon_tweet.text
        #NLP score for tweet
        elon_sentiment = comprehend.detect_sentiment(Text=elon_tweet_text,LanguageCode='en')['Sentiment']
        #ByBit cart link for tweet
        #notification?
        http_response = {
            "statusCode": 200,
            "headers": {
                'Access-Control-Allow-Origin': '*',
            },
            "body": json.dumps({
                "tweet_url": tweet_url,
                "valid_elon_tweet":"true",
                "mentioned_stonks_or_coins": "none",
                "elon_sentiment": elon_sentiment,
                "text": elon_tweet_text,
                "bybit_link": get_bybit_link()
            })
        }
    except Exception as e:
        print(e)
        http_response = {
            "statusCode": 500,
            "headers": {
                'Access-Control-Allow-Origin': '*',
            },
            "body": json.dumps({"error": e})
        }
    return http_response
