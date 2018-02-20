import numpy as np
import pandas as pd
from iso639 import languages

CUR_DB = '../title.akas.tsv'
BIG_DB = 'title.basics_episode_final.csv'
ID_LIST = 'PictureID_list.txt'
REQ_DB_1 = 'title.languages.csv'
REQ_DB_2 = 'title.basics_episode_final.csv'
cur_db = pd.read_csv(CUR_DB, sep='\t',
                     usecols=['titleId', 'language'], low_memory=False)

cur_db.rename(columns={
                        'titleId': 'PictureID',
                        'language': 'Language'
                      },
              inplace=True)

# Remove NULL locations
cur_db = cur_db.loc[cur_db['Language'] != '\\N']

def iso_coding(arr):
    try:
        if len(arr) == 2:
            return languages.get(part1=arr).name
        elif len(arr) == 3:
            return languages.get(part3=arr).name
    except:
        return '\\N'

cur_db['Language'] = cur_db['Language'].apply(iso_coding)

# Remove NULL locations again
cur_db = cur_db.loc[cur_db['Language'] != '\\N']

id_list = np.genfromtxt(ID_LIST, dtype=str).reshape(-1).tolist()
cur_db = cur_db.loc[cur_db['PictureID'].isin(id_list)]
cur_db.drop_duplicates(inplace=True)

big_db = pd.read_csv(BIG_DB, sep=',',
                     usecols=['PictureID', 'Language'], low_memory=False)
big_db = big_db.loc[big_db['Language'] != '\\N']
big_db['Language'] = big_db['Language'].apply(iso_coding)

req_db = cur_db.append(big_db, ignore_index=True)
req_db.drop_duplicates(inplace=True)
req_db.sort_values(by=['PictureID'], inplace=True)

req_db.to_csv(REQ_DB_1, sep=',', na_rep='\\N', index=False)

del req_db
del big_db
del cur_db

# Remove Language from title.basics_episode_required.csv
req_db = pd.read_csv(BIG_DB, sep=',', low_memory=False)
req_col_list = req_db.columns.tolist()
req_col_list.remove('Language')
req_db.to_csv(REQ_DB_2, sep=',', index=False, columns=req_col_list)
