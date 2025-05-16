# ai_agent/twitter_integration/content_creation.py

def create_tweet(game_name, game_rating):
    """Creates a tweet about a game."""
    tweet = f"Just reviewed {game_name}! Our AI gives it a rating of {game_rating}/10.  Check it out! #web3gaming #AI #GameReview"
    return tweet

if __name__ == '__main__':
    print(create_tweet("AwesomeWeb3Game", 8.5))
