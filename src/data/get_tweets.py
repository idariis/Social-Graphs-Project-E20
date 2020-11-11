#%%
import pandas as pd
import numpy as np
import tweepy
import datetime
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

for j, congrees in enumerate(all_congress):
    print(info[j], j, '/', 4)

    for i in trange(len(congrees) // 100):

        ids = list(congrees[i * 100 : i * 100 + 100])
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
            for t in api.statuses_lookup(id_=ids)
        ]
        results.extend(response)
        
#%%
tweets_congress = pd.DataFrame(
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

tweets_congress.to_csv('../../Data/Interim/tweets_congress.csv')

# %%
