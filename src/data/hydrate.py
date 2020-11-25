import pandas as pd
import numpy as np
import tweepy
import datetime
import time
import re
from tqdm import trange


def hydrate_tweets(tweet_ids, filepath, api):

    exception_list = []
    results = []
    backoff_counter = 1
    for i in trange(len(tweet_ids) // 100):

        while True:
            try:

                ids = list(tweet_ids[i * 100 : i * 100 + 100])
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
            print("Updating local file")
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
        
        tweets_congres.to_pickle(filepath)


if __name__ == "__main__":
    from src.tools.twitter_api import auth

    api = tweepy.API(auth, wait_on_rate_limit=True)

    representatives115 = np.loadtxt(
        "../Data/Raw/Tweets/representatives115.txt", dtype=int
    )
    representatives116 = np.loadtxt(
        "../Data/Raw/Tweets/representatives116.txt", dtype=int
    )
    senators115 = np.loadtxt("../Data/Raw/Tweets/senators115.txt", dtype=int)
    senators116 = np.loadtxt("../Data/Raw/Tweets/senators116.txt", dtype=int)
    trump = np.loadtxt("../Data/Raw/Tweets/trump_id.txt", dtype=int)


    congress = representatives115 + representatives116 + senators115 + senators116 + trump
    filepath = "Data/interim/tmp.pkl"

    hydrate_tweets(
        tweet_ids=congress,
        filepath=filepath,
        api = api
    )
    
