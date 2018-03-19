import sys
import numpy as np
import pandas as pd

PIC_LIST_ROOT = 'PictureID_list.txt'
PER_LIST_ROOT = 'PersonID_list.txt'
GIVEN_FILE = sys.argv[1]
EXT = GIVEN_FILE[-3:]
REQ_FILE = GIVEN_FILE[:-4] + '_crossref.csv'
if EXT == 'tsv':
    SEP = '\t'
elif EXT == 'csv':
    SEP = ','

cur_db = pd.read_csv(GIVEN_FILE, sep=SEP, low_memory=False)
print("Before cross-referencing: {}".format(len(cur_db)))

if 'PictureID' in cur_db.columns.tolist():
    pic_list = np.genfromtxt(PIC_LIST_ROOT, dtype=str).tolist()
    cur_db = cur_db.loc[cur_db['PictureID'].isin(pic_list)]
    del pic_list
    print("After cross-referencing PictureID: {}".format(len(cur_db)))

if 'PersonID' in cur_db.columns.tolist():
    per_list = np.genfromtxt(PER_LIST_ROOT, dtype=str).tolist()
    cur_db = cur_db.loc[cur_db['PersonID'].isin(per_list)]
    del per_list
    print("After cross-referencing PersonID: {}".format(len(cur_db)))

cur_db.to_csv(REQ_FILE, sep=',', index=False)
