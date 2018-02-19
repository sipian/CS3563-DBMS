import pandas as pd

cur_db = pd.read_csv('name.basics.tsv', sep='\t',
                     usecols=['nconst', 'primaryName', 'birthYear', 'deathYear'],
                     low_memory=False)

cur_db.rename(columns={
                        'nconst': 'PersonID',
                        'primaryName': 'PersonName',
                        'birthYear': 'BirthYear',
                        'deathYear': 'DeathYear'
                      },
              inplace=True)

cur_db.to_csv('title.person.csv', sep=',', index=False)
nid_list = cur_db['PersonID'].tolist()
nid_file = open('PersonID_list.txt', 'w')
for ID in nid_list:
    nid_file.write('{}\n'.format(ID))
nid_file.close()
