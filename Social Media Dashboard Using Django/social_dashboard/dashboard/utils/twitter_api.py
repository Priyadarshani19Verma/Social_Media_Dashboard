import tweepy
import time
from . import twitter_credentials  # this imports the token from twitter_credentials.py

# In-memory cache
CACHE = {
    'tweets': None,
    'last_fetched': 0
}
CACHE_TIMEOUT = 300  # Cache tweets for 5 minutes (300 seconds)

def get_tweets(username):
    current_time = time.time()

    # If cached tweets are still fresh, return them
    if CACHE['tweets'] and (current_time - CACHE['last_fetched'] < CACHE_TIMEOUT):
        return CACHE['tweets']

    # Twitter setup using Bearer Token
    client = tweepy.Client(bearer_token=twitter_credentials.BEARER_TOKEN)

    try:
        user_info = client.get_user(username=username) # type: ignore
        user_id = user_info.data.id
        tweets_response = client.get_users_tweets(id=user_id, max_results=10)
        tweet_list = []
        if tweets_response.data:
            for tweet in tweets_response.data:
                tweet_list.append({'text': tweet.text})

        # Save to cache
        CACHE['tweets'] = tweet_list
        CACHE['last_fetched'] = current_time

        return tweet_list

    except tweepy.TooManyRequests:
        print("⚠️ Twitter rate limit reached. Try again later.")
        return []

    except Exception as e:
        print("❌ Error fetching tweets:", e)
        return []

