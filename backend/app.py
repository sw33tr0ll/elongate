import json
import tweepy
import boto3

ssm_client = boto3.client('ssm')

try:
    api_key = ssm_client.get_parameter(Name='elongate_api_key')
    api_secret_key = ssm_client.get_parameter(Name='elongate_api_secret_key')
    access_token = ssm_client.get_parameter(Name='elongate_access_token')
    access_token_secret = ssm_client.get_parameter(Name='elongate_access_token_secret')
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
        if '?' in post_data['tweet']:
            tweet_url = post_data['tweet'].split('?')[0]                # remove ? from tweet
        else:
            tweet_url = post_data['tweet']
        tweet_id = tweet_url.split('/')[-1]
        auth = tweepy.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        elon_tweet = api.get_status(tweet_id)
        print(f"found elon tweet :: {elon_tweet}")
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
