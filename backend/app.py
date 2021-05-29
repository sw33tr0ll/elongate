import json

def analyze_tweet(event, _):
    print(event)
    try:
        tweet_url = event['body']
        http_response = {
            "statusCode": 200,
            "headers": {
                'Access-Control-Allow-Origin': '*',
            },
            "body": json.dumps({"tweet": tweet_url,"elon":"true"})
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
