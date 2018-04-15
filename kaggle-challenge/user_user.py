import psycopg2
import numpy as np
import pandas as pd

conn = psycopg2.connect("dbname=friendship1 user=postgres password=Sahil23!" )
cur = conn.cursor()


def _get_individual_info(userid, cur, total=220969):
    """
    Gets a rating-hot-vector for a given user id from a pool of items
    """
    # Assume the data frame is in Pandas for now, named "cur_db"

    # req = cur_db.loc[cur_db['UserId'] == userid, ['ForUserId', 'Rating']]
    # idxs = req['ForUserId'].tolist()
    # rats = req['Rating'].tolist()

    cur.execute("SELECT * FROM Train_Ratings WHERE userid = "+str(userid)+";")
    rows = cur.fetchall()
    rows = np.array([list(i) for i in rows])
    idxs = rows[:,1]
    rats = rows[:,2]

    # rhe stands for "rating hot encoding"
    rhe = np.zeros((total,))
    rhe[idxs] = rats
    return rhe

def get_batch_info(userids, total=220969):
    """
    Gets a matrix of rating-hot-vectors for a given list of user ids from a pool of items
    """
    batch_matrix = np.zeros((len(userids), total))
    for i, uid in enumerate(userids):
        batch_matrix[i] = _get_individual_info(uid, total)
    return batch_matrix

print(_get_individual_info(23408,cur))