#%%
import pandas as pd
import numpy as np
import tweepy
import pickle
import datetime
from tqdm import trange
from src.tools.twitter_api import auth


api = tweepy.API(auth, wait_on_rate_limit=True)

#%%
medias = pd.read_table('../../Data/Raw/LargestMedia.csv', sep=';')
userIDs = medias['Twitter name'].values
#%%
# screen name of the account to be fetched

media_twitter_dict = dict()

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
    while True:
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

    media_twitter_dict[userID] = all_tweets

# %%
with open('../../Data/Interim/media_twitter.pickle', 'wb') as handle:
    pickle.dump(media_twitter_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


# %%
