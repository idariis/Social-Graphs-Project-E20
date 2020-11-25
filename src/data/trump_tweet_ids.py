# importing the module 
import pandas as pd

  
def get_trump_tweet_ids(df_trump, filepath):
    """
    Extract the tweet id from a dataframe downloaded at trump twitter archive.
    """
    # Remove rows with missing values
    df_trump = df_trump[~df_trump.isna().any(axis=1)]

    # Extract the tweets ids and convert them to integers
    trump_ids = list(df_trump.id_str.astype(int).values)

    with open(filepath, 'w') as output:
        for row in trump_ids:
            output.write(str(row) + '\n')

        print(f'{len(trump_ids)} tweet ids saved.')


if __name__ == "__main__":
    print('')
    print('__file__:    ', __file__)
    df_trump_tweets1 = pd.read_csv('Data/raw/tweets/trump_tweets_1st.csv')  
    df_trump_tweets2 = pd.read_csv('Data/raw/tweets/trump_tweets_1st.csv')
    df_trump = pd.concat([df_trump_tweets1, df_trump_tweets2])

    filepath = "Data/raw/tweets/trump_id.txt"
    get_trump_tweet_ids(df_trump, filepath)