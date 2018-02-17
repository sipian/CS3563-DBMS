import numpy as np
import pandas as pd
from iso3166 import countries

CUR_DB = 'title.akas.tsv'
ID_LIST = 'PictureID_list.txt'
REQ_DB = 'title.location.csv'
cur_db = pd.read_csv(CUR_DB, sep='\t',
                     usecols=['titleId', 'region'], low_memory=False)

cur_db.rename(columns={
                        'titleId': 'PictureID',
                        'region': 'Region'
                      },
              inplace=True)

# Remove NULL locations
cur_db = cur_db.loc[cur_db['Region'] != '\\N']
def iso_coding(arr):
    try:
        return countries.get(arr).name
    except:
        return '\\N'

cur_db['Region'] = cur_db['Region'].apply(iso_coding)
# Remove NULL locations again
cur_db = cur_db.loc[cur_db['Region'] != '\\N']

id_list = np.genfromtxt(ID_LIST, dtype=str).reshape(-1).tolist()

cur_db.loc[cur_db['PictureID'].isin(id_list)].to_csv(REQ_DB, sep=',', na_rep='\\N', index=False)
