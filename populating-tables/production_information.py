import ast
import pandas as pd

cur_db = pd.read_csv('title.basics_episode.tsv', sep='\t',
                     usecols=['tconst', 'production_companies', 'production_countries'],
                     low_memory=False)

cur_db_to_records = cur_db.to_records()

companies_dict = {'tconst': [], 'CompanyID': [], 'CompanyName': []}
countries_dict = {'tconst': [], 'CountryName': []}

ID = cur_db.columns.tolist().index('tconst') + 1
COMP = cur_db.columns.tolist().index('production_companies') + 1
COUN = cur_db.columns.tolist().index('production_countries') + 1

for rec in cur_db_to_records:
    # Company processing
    if rec[COMP] != "\\N":
        json_obj = ast.literal_eval(rec[COMP])
        if isinstance(json_obj, list):
            for indi in json_obj:
                companies_dict['tconst'].append(rec[ID])
                companies_dict['CompanyID'].append(indi['id'])
                companies_dict['CompanyName'].append(indi['name'])
        elif isinstance(json_obj, dict):
            companies_dict['tconst'].append(rec[ID])
            companies_dict['CompanyID'].append(json_obj['id'])
            companies_dict['CompanyName'].append(json_obj['name'])

    # Country processing
    if rec[COUN] != "\\N":
        json_obj = ast.literal_eval(rec[COUN])
        if isinstance(json_obj, list):
            for indi in json_obj:
                countries_dict['tconst'].append(rec[ID])
                countries_dict['CountryName'].append(indi['name'])
        elif isinstance(json_obj, dict):
            countries_dict['tconst'].append(rec[ID])
            countries_dict['CountryName'].append(json_obj['name'])

companies = pd.DataFrame(companies_dict, columns=sorted(companies_dict.keys(), reverse=True))
companies.to_csv('./title.production_comp.tsv', sep='\t', na_rep="\\N", index=False, header=['tconst', 'CompanyName', 'CompanyID'])

countries = pd.DataFrame(countries_dict, columns=sorted(countries_dict.keys(), reverse=True))
countries.to_csv('./title.countries.tsv', sep='\t', na_rep="\\N", index=False, header=['tconst', 'CountryName'])
