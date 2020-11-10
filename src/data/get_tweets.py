#%%
import pandas as pd
import numpy as np
import tweepy
import datetime
from tqdm import trange
from src.tools.twitter_api import auth


api = tweepy.API(auth, wait_on_rate_limit=True)
#%%

# screen name of the account to be fetched
userIDs = ["CNN", "foxnews", "BreitbartNews"]
end_date = datetime.datetime(2020, 1, 3, 0, 0, 0)

for userID in userIDs:
    print(userID)
    # fetching the statuses
    tweets = api.user_timeline(
        screen_name=userID,
        # 200 is the maximum allowed count
        count=200,
        include_rts=False,
        # Necessary to keep full_text
        # otherwise only the first 140 words are extracted
        tweet_mode="extended",
    )

    all_tweets = []
    all_tweets.extend(tweets)
    oldest_id = tweets[-1].id

    # exstract all tweets since the ea
    while tweets[-1].created_at > end_date:
        tweets = api.user_timeline(
            screen_name=userID,
            # 200 is the maximum allowed count
            count=200,
            include_rts=False,
            max_id=oldest_id - 1,
            # Necessary to keep full_text
            # otherwise only the first 140 words are extracted
            tweet_mode="extended",
        )
        if len(tweets) == 0:
            break
        oldest_id = tweets[-1].id
        all_tweets.extend(tweets)

        print("N of tweets downloaded till now {}".format(len(all_tweets)))
# %%

tweets 

# %%
userID = "peterfalktoft"
tweets = api.user_timeline(
        screen_name=userID,
        # 200 is the maximum allowed count
        count=200,
        include_rts=False,
        max_id=1246490680052125707 - 1,
        # Necessary to keep full_text
        # otherwise only the first 140 words are extracted
        tweet_mode="extended",
    )




# %%
tweets[0]

# %%
