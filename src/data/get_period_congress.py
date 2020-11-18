#%%
import pickle
import pandas as pd

#%%
# Representatives 115
with open('../../Data/Interim/representatives115.pkl', 'rb') as rep_115:
    rep_115 = pickle.load(rep_115)

rep_115 = rep_115.sort_values(by="created_at").reset_index(drop=True)
rep_115 = rep_115.iloc[787068:1424919]

#%%
# Representatives 116
with open('../../Data/Interim/representatives116.pkl', 'rb') as rep_116:
    rep_116 = pickle.load(rep_116)

rep_116 = rep_116.sort_values(by="created_at").reset_index(drop=True)
rep_116 = pd.concat([rep_116.iloc[560022:1275510], rep_116.iloc[1326805:2084058]])

#%%
# Senators 115
with open('../../Data/Interim/senators115.pkl', 'rb') as sen_115:
    sen_115 = pickle.load(sen_115)

sen_115 = sen_115.sort_values(by="created_at").reset_index(drop=True)
sen_115 = sen_115.iloc[270119:505059]

#%% 
# Senators 116
with open('../../Data/Interim/senators116.pkl', 'rb') as sen_116:
    sen_116 = pickle.load(sen_116)

sen_116 = sen_116.sort_values(by="created_at").reset_index(drop=True)
sen_116 = pd.concat([sen_116.iloc[175373:441589], sen_116.iloc[457421:687004]])

#%% 
congress = pd.concat([rep_115, rep_116, sen_115, sen_116]) 
file_name = 'congress'
congress.to_pickle(
        "../../Data/Interim/" + file_name + ".pkl"
    )
# %%
