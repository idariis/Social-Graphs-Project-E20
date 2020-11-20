# importing the module 
import pandas as pd

df_trump_tweets = pd.read_csv('../../data/raw/tweets/trump.csv')  

trump_ids = list(df_trump_tweets.id.astype(int).values)

with open("../../data/raw/tweets/trump_id.txt", 'w') as output:
    for row in trump_ids:
        output.write(str(row) + '\n')