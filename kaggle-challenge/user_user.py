import numpy as np
import pandas as pd

def _get_individual_info(userid, total=220969):
    """
    Gets a rating-hot-vector for a given user id from a pool of items
    """
    # Assume the data frame is in Pandas for now, named "cur_db"
    req = cur_db.loc[cur_db['UserId'] == userid, ['ForUserId', 'Rating']]
    idxs = req['ForUserId'].tolist()
    rats = req['Rating'].tolist()

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
