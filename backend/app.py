import json

def analyze_tweet(event, _):
    tweet_url = event['body']
    http_response = {
        "statusCode": 200,
        "body": json.dumps({"tweet": tweet_url,"elon":"true"})
    }
    return http_response