import json
import tweepy
from utils import aws

try:
    consumer_key = aws.get_from_ssm('elongate_consumer_key')
    consumer_secret = aws.get_from_ssm('elongate_consumer_secret')
    access_token = aws.get_from_ssm('elongate_access_token')
    access_token_secret = aws.get_from_ssm('elongate_access_token_secret')
except Exception as e:
    print("failed to get twitter keys from SSM! exiting...")

def check_tweet(event, _):
    return {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Origin': '*',
        },
        "body": json.dumps({"coming soon": "coming_soon"})
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
        tweet_url = post_data['tweet']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        #regex elon tweet link
        #check if tweet is live
        #check if tweet mentions stonk/coin
        #NLP score for tweet
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
                "sentiment": "none",
                "bitbuy_link": "none"
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
