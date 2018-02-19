import numpy as np
import pandas as pd
from iso639 import languages

CUR_DB = 'title.akas.tsv'
ID_LIST = 'PictureID_list.txt'
REQ_DB = 'title.languages.csv'
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
cur_db.loc[cur_db['PictureID'].isin(id_list)].to_csv(REQ_DB, sep=',', na_rep='\\N', index=False)
