#%%
import pandas as pd
import numpy as np
import tweepy
import datetime
import time
import re
from tqdm import trange
from src.tools.twitter_api import auth
#%% 
api = tweepy.API(auth, wait_on_rate_limit=True)
#%%
trump_tweets_1st = pd.read_table('../../Data/Raw/Tweets/trump_tweets_1st.csv', sep=',')
trump_tweets_2nd = pd.read_table('../../Data/Raw/Tweets/trump_tweets_2nd.csv', sep=',')

trump = pd.concat([trump_tweets_1st, trump_tweets_2nd])

#%% 
# Removing Nan's 
trump.dropna(inplace=True)
# %%
# Converting 'id_str' to int
trump['id_str'] = [int(id_str) for id_str in trump['id_str']]

# %%
# Get trump tweets
exception_list = []
results = []
backoff_counter = 1
file_name = 'trump'

for i in trange(len(trump['id_str']) // 100):

    while True:
        try:

            ids = list(trump['id_str'][i * 100 : i * 100 + 100])
            for t in api.statuses_lookup(id_=ids, tweet_mode="extended"):

                if hasattr(t, "retweeted_status"):
                    full_text = t.retweeted_status.full_text
                    try:
                        retweet = re.findall(r"^RT @([^:]+):", t.full_text)[0] 
                    except:
                        exception_list.append(t.id)
                        continue

                else:  # Not a Retweet
                    full_text = t.full_text
                    retweet = False

                response = (
                    t.user.id,
                    t.user.name,
                    t.id,
                    t.created_at,
                    full_text,
                    retweet,
                    t.retweet_count,
                    t.favorite_count,
                    t.in_reply_to_status_id,
                    t.in_reply_to_user_id,
                )

                results.append(response)

        except tweepy.TweepError as e:
            print(e.reason)
            print("Sleeping for {} seconds".format(60 * backoff_counter))
            time.sleep(60 * backoff_counter)
            backoff_counter += 1

        else:
            break
#%%
tweets_congres = pd.DataFrame(
    results,
    columns=[
        "user_id",
        "user_name",
        "id",
        "created_at",
        "text",
        "retweet",
        "retweet_count",
        "favorite_count",
        "in_reply_to_status_id",
        "in_reply_to_user_id",
    ],
)
tweets_congres.to_pickle(
        "../../Data/Interim/" + file_name + ".pkl"
    )
# %%
