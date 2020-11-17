# importing the module 
import json 
  
# Opening JSON file 
with open('../../data/raw/tweets/trump.json') as json_file: 
    data = json.load(json_file) 

trump_ids = []
for tweet in data:
    trump_ids.append(tweet['id'])

with open("../../data/raw/tweets/trump_id.txt", 'w') as output:
    for row in trump_ids:
        output.write(str(row) + '\n')