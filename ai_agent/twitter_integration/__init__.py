# ai_agent/twitter_integration/twitter_api.py
import tweepy

# Replace with your actual API keys and tokens
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token =  'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOdgJIQw4kH%2BTkF0KI%3D1dZ2AzUHfmCc8VvSEHfq6hEjIuDZr8AVeHAJ3tfnsggJ9NXy96'
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

def post_tweet(content):
    """Posts a tweet to Twitter."""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        api.update_status(content)
        print("Tweet posted successfully!")
    except tweepy.TweepyException as e:
        print(f"Error posting tweet: {e}")

if __name__ == '__main__':
    post_tweet("Hello, world! This is a test tweet from my AI Agent.")
