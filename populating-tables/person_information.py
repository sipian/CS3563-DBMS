import pandas as pd

cur_db = pd.read_csv('name.basics.tsv', sep='\t',
                     usecols=['nconst', 'primaryName', 'birthYear', 'deathYear'],
                     low_memory=False)

cur_db_to_records = cur_db.to_records()

person_dict = {'PersonID': [], 'PersonName': [], 'BirthYear': [], 'DeathYear': []}

ID = cur_db.columns.tolist().index('nconst') + 1
NAME = cur_db.columns.tolist().index('primaryName') + 1
BIRTH = cur_db.columns.tolist().index('birthYear') + 1
DEATH = cur_db.columns.tolist().index('deathYear') + 1

for rec in cur_db_to_records:
    # Person processing
    person_dict['PersonID'].append(rec[ID])
    person_dict['PersonName'].append(rec[NAME])
    person_dict['BirthYear'].append(rec[BIRTH])
    person_dict['DeathYear'].append(rec[DEATH])

persons = pd.DataFrame(person_dict, columns=sorted(person_dict.keys(), reverse=True))
persons.to_csv('./title.person.tsv', sep='\t', na_rep="\\N", index=False, header=['PersonName', 'PersonID', 'DeathYear', 'BirthYear'])
