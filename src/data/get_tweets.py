#%%
import pandas as pd
import numpy as np
import tweepy
import datetime
import time
from tqdm import trange
from src.tools.twitter_api import auth


api = tweepy.API(auth, wait_on_rate_limit=True)
#%%
representatives115 = np.loadtxt(
    "../../Data/Raw/Tweets/representatives115.txt", dtype=int
)
representatives116 = np.loadtxt(
    "../../Data/Raw/Tweets/representatives116.txt", dtype=int
)

senators115 = np.loadtxt(
    "../../Data/Raw/Tweets/senators115.txt", dtype=int
)

senators116 = np.loadtxt(
    "../../Data/Raw/Tweets/senators116.txt", dtype=int
)

all_congress = [representatives115, representatives116, senators115, senators116]
info = ['representatives115', 'representatives116', 'senators115', 'senators116']
#%%

results = []
backoff_counter = 1
for k, congress in enumerate(all_congress):
    print(info[k])
    for i in trange(len(congress) // 100):
        try:
            ids = list(congress[i * 100 : i * 100 + 100])

            for t in api.statuses_lookup(id_=ids):
                response = [
                    (
                        t.user.id,
                        t.user.name,
                        t.id,
                        t.created_at,
                        t.text,
                        t.retweet_count,
                        t.favorite_count,
                        t.in_reply_to_status_id,
                        t.in_reply_to_user_id,
                    )
                ]
                results.extend(response)

        except tweepy.TweepError as e:
            print(e.reason)
            print("Sleeping for {} seconds".format(60*backoff_counter))
            time.sleep(60*backoff_counter)
            backoff_counter += 1
            continue

tweets_congres_all = pd.DataFrame(
    results,
    columns=[
        "user_id",
        "user_name",
        "id",
        "created_at",
        "text",
        "retweet_count",
        "favorite_count",
        "in_reply_to_status_id",
        "in_reply_to_user_id",
    ],
)
tweets_congres_all.to_csv('../../Data/Interim/tweets_congress_all.csv')


# %%
