import tweepy

api_key = ""
api_secret_key = ""

bearer_token = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)

try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')
