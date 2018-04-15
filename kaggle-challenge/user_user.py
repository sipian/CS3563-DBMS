import psycopg2
import numpy as np
import pandas as pd
import scipy.spatial as ssp

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

def similarity_batch_individual(batch_userids, given_userid, cur_db, dist='cosine', total=220969):
    """
    Computes a similarity between items chosen a batch of users and a user
    """
    mat = get_batch_info(batch_userids, cur_db, dist, total)
    vec = _get_individual_info(given_userid, cur_db, dist, total)
    sims = ssp.distance.cdist(mat, vec.reshape(1, -1), dist)
    return sims

def similarity_batch_batch(batch_userids, batch_given_userids, cur_db, dist='cosine', total=220969):
    """
    Computes a similarity between items chosen by two batches of users
    """
    mat1 = get_batch_info(batch_userids, cur_db, dist, total)
    mat2 = get_batch_info(batch_given_userids, cur_db, dist, total)
    sims = ssp.distance.cdist(mat1, mat2, dist)
    return sims

def predict_individual(given_userid, given_itemid, cur_db, dist='cosine', total=220969):
    """
    Predicts the value for a user-item pair
    """
    req_users = cur_db.loc[cur_db['ForUserId'] == given_itemid, ['UserId', 'Rating']]
    userlist = req_users['UserId'].tolist()
    ratings = req_users['Rating'].tolist()
    req_sim = similarity_batch_individual(userlist, given_userid, cur_db, dist, total).reshape(-1)
    return np.dot(ratings, req_sim) / req_sim.sum()

def predict_batch(given_userids, given_itemid, cur_db, dist='cosine', total=220969):
    """
    Predicts the value for a list of pairs [(u1, i), (u2, i), (u3, i), ..., (un, i)]
    """
    req_users = cur_db.loc[cur_db['ForUserId'] == given_itemid, ['UserId', 'Rating']]
    userlist = req_users['UserId'].tolist()
    ratings = np.array(req_users['Rating'].tolist())
    req_sim = similarity_batch_batch(userlist, given_userids, cur_db, dist, total)
    return ratings.dot(req_sim) / req_sim.sum(0)

def get_users_for_item(given_itemid, cur_db):
    """
    Get a list of users paired with an item in the DB
    """
    return cur_db.loc[cur_db['ForUserId'] == given_itemid, 'UserId'].tolist()
