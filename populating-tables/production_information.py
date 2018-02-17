import ast
import numpy as np
import pandas as pd
from iso3166 import countries

CUR_DB = 'title.basics_episode.tsv'
ID_LIST = 'PictureID_list.txt'
REQ_DB_1 = 'title.production_comp.csv'
REQ_DB_2 = 'title.filming_location.csv'
cur_db = pd.read_csv(CUR_DB, sep='\t',
                     usecols=['tconst', 'production_companies', 'production_countries'],
                     low_memory=False)

cur_db_to_records = cur_db.to_records()

companies_dict = {'PictureID': [], 'CompanyID': [], 'CompanyName': []}
countries_dict = {'PictureID': [], 'CountryName': []}

ID = cur_db.columns.tolist().index('tconst') + 1
COMP = cur_db.columns.tolist().index('production_companies') + 1
COUN = cur_db.columns.tolist().index('production_countries') + 1

def fix_country_name(country):
    if country == 'United States of America':
        return 'United States'
    elif country == 'United Kingdom':
        return 'United Kingdom of Great Britain and Northern Ireland'
    return country

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

    if rec[COUN] != "\\N":
        json_obj = ast.literal_eval(rec[COUN])
        if isinstance(json_obj, list):
            for indi in json_obj:
                countries_dict['PictureID'].append(rec[ID])
                try:
                    cname = countries.get(indi['iso_3166_1']).name
                except:
                    cname = indi['name']
                cname = fix_country_name(cname)
                countries_dict['CountryName'].append(cname)
        elif isinstance(json_obj, dict):
            countries_dict['PictureID'].append(rec[ID])
            try:
                cname = countries.get(json_obj['iso_3166_1']).name
            except:
                cname = json_obj['name']
            cname = fix_country_name(cname)
            countries_dict['CountryName'].append(cname)

# Free RAM
del cur_db

id_list = np.genfromtxt(ID_LIST, dtype=str).reshape(-1).tolist()

companies = pd.DataFrame(companies_dict, columns=sorted(companies_dict.keys(), reverse=True))
companies.loc[companies['PictureID'].isin(id_list)].to_csv(REQ_DB_1, sep=',', na_rep="\\N",
                                                           index=False, header=['PictureID', 'CompanyName', 'CompanyID'])

countries = pd.DataFrame(countries_dict, columns=sorted(countries_dict.keys(), reverse=True))
countries.loc[countries['PictureID'].isin(id_list)].to_csv(REQ_DB_2, sep=',', na_rep="\\N",
                                                           index=False, header=['PictureID', 'CountryName'])
