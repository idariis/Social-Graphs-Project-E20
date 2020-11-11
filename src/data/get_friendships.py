# %%
#%%
import pandas as pd
import numpy as np
import tweepy
import datetime
from tqdm import trange
from src.tools.twitter_api import auth


api = tweepy.API(auth, wait_on_rate_limit=True)

#%%
api.show_friendship(
    source_id = 172858784, 
    target_id = 432895323
    )