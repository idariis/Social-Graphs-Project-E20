import pandas as pd

congress = pd.read_pickle('Data/Interim/congress.pkl')
twitter_handles = pd.read_table('Data/Processed/Twitter_Handles_updated.csv', sep = ',')

s1 = set(twitter_handles['twitter_display_name'])

# Make sure tweets only comes from people that twitter handles exist for. 
congress = congress[congress.user_name.isin(s1)]

# Keep only the periods from Harward:
mask = (
    #January 27, 2017 and January 2, 2019 
    (congress.created_at > '2017-1-27 00:00:00') & (congress.created_at < '2019-1-2 00:00:00')
    | 
    #January 27, 2019 and May 7, 2020 
    (congress.created_at > '2019-1-27 00:00:00') & (congress.created_at < '2020-5-7 00:00:00')
)
congress = congress[mask]
congress = congress.drop_duplicates(keep='first')
congress = congress.sort_values(by='created_at')
congress = congress.reset_index(drop=True)
congress.to_pickle("Data/interim/congress_cleaned.pkl")


# Extract the tweets ids and convert them to integers
ids = list(congress.id.astype(int).values)

filepath = "Data/raw/tweets/Cleaned_tweet_id.txt"
with open(filepath, 'w') as output:
    for row in ids:
        output.write(str(row) + '\n')

    print(f'{len(ids)} tweet ids saved.')