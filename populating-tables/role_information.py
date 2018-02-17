import numpy as np
import pandas as pd

REQ_DB = 'title.principals.tsv'
REQ_DB_MOD = 'title.principals_required.csv'
ID_LIST = 'PictureID_list.txt'

cur_db = pd.read_csv(REQ_DB, sep='\t', na_values='\\N', usecols=['tconst', 'nconst', 'category'])
cur_db.rename(columns={
                       'tconst': 'PictureID',
                       'nconst': 'PersonID',
                       'category': 'Role'
                      },
              inplace=True)

# Rules to be followed:
# 1. Crew: Cinematographer, Editor, Production Designer
# 2. Actor: Actor, Actress
# 3. Director: Director
# 4. Writer: Writer
# 5. Music: Composer
# 6. Producer: Producer
# 7. Miscellaneous: Self, Archive Footage, Archive Sound
cur_db.loc[((cur_db['Role'] == 'cinematographer') |
            (cur_db['Role'] == 'editor') |
            (cur_db['Role'] == 'production_designer')),
           'Role'] = 'Crew'
cur_db.loc[((cur_db['Role'] == 'actor') |
            (cur_db['Role'] == 'actress')),
           'Role'] = 'Actor'
cur_db.loc[cur_db['Role'] == 'director', 'Role'] = 'Director'
cur_db.loc[cur_db['Role'] == 'writer', 'Role'] = 'Writer'
cur_db.loc[cur_db['Role'] == 'composer', 'Role'] = 'Music'
cur_db.loc[cur_db['Role'] == 'producer', 'Role'] = 'Producer'
cur_db.loc[((cur_db['Role'] == 'self') |
            (cur_db['Role'] == 'archive_footage') |
            (cur_db['Role'] == 'archive_sound')),
           'Role'] = 'Miscellaneous'

id_list = np.genfromtxt(ID_LIST, dtype=str).reshape(-1).tolist()

# Agreed, below select is very inefficient
cur_db.loc[cur_db['PictureID'].isin(id_list)].to_csv(REQ_DB_MOD, sep=',', na_rep='\\N', index=False)
