import ast
import numpy as np
import pandas as pd

CUR_DB = 'title.basics_episode.tsv'
ID_LIST = 'PictureID_list.txt'
REQ_DB = 'title.production_comp.csv'
cur_db = pd.read_csv(CUR_DB, sep='\t',
                     usecols=['tconst', 'production_companies'],
                     low_memory=False)

cur_db_to_records = cur_db.to_records()

companies_dict = {'PictureID': [], 'CompanyID': [], 'CompanyName': []}

ID = cur_db.columns.tolist().index('tconst') + 1
COMP = cur_db.columns.tolist().index('production_companies') + 1

for rec in cur_db_to_records:
    # Company processing
    if rec[COMP] != "\\N":
        json_obj = ast.literal_eval(rec[COMP])
        if isinstance(json_obj, list):
            for indi in json_obj:
                companies_dict['PictureID'].append(rec[ID])
                companies_dict['CompanyID'].append(indi['id'])
                companies_dict['CompanyName'].append(indi['name'])
        elif isinstance(json_obj, dict):
            companies_dict['PictureID'].append(rec[ID])
            companies_dict['CompanyID'].append(json_obj['id'])
            companies_dict['CompanyName'].append(json_obj['name'])

# Free RAM
del cur_db

companies = pd.DataFrame(companies_dict, columns=sorted(companies_dict.keys(), reverse=True))
id_list = np.genfromtxt(ID_LIST, dtype=str).reshape(-1).tolist()
companies.loc[companies['PictureID'].isin(id_list)].to_csv(REQ_DB, sep=',', na_rep="\\N",
                                                           index=False, header=['PictureID', 'CompanyName', 'CompanyID'])
