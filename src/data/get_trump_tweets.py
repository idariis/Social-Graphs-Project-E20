import pandas as pd
import numpy as np
import tweepy
import datetime
import time
import re
from tqdm import trange
from src.tools.twitter_api import auth
#%%
trump1 = pd.read_csv('../../Data/Raw/tweets/trump_tweets_1st.csv')
trump1.drop(trump1.tail(1).index,inplace=True)

trump2 = pd.read_csv('../../Data/Raw/tweets/trump_tweets_2nd.csv')
trump2.drop(trump2.tail(1).index,inplace=True)

trump = pd.concat([trump1, trump2]).reset_index(drop=True)
# %%

tweets_id = [int(tweet_id) for tweet_id in trump[trump.id_str.notna()].id_str.to_list()]

# %%
file_name = 'trump'

for i in trange(len(tweets_id) // 100):

    while True:
        try:

            ids = list(congress_tweets[i * 100 : i * 100 + 100])
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

    if i % 100 == 0:
        print('Updating local file')
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
#