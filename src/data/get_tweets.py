#%%
import pandas as pd
import numpy as np
import tweepy
import datetime
from tqdm import trange
from src.tools.twitter_api import auth


api = tweepy.API(auth, wait_on_rate_limit=True)
#%%


#%%

results = []

for i in trange(len(df)//100):

    ids = list(df["tweet_id"].iloc[i*100:i*100+100])
    response = [
            (t.id, t.created_at, t.text) 
            for t in api.statuses_lookup(id_=ids)]

    results.extend(response)

#%%
tweets_200316 = pd.DataFrame(
    results, columns=['tweet_id', 'date_time', 'tweet']
)