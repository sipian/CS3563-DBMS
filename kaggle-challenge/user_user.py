import os
import sys
import psycopg2
import threading
import numpy as np
import pandas as pd
import scipy.spatial as ssp
import multiprocessing as mp

from threading import Thread
from multiprocessing import Process

no_of_thread = 4

def _get_individual_info(userid, dist, total):
    """
    Gets a rating-hot-vector for a given user id from a pool of items
    """
    req = tr_data.loc[tr_data['UserId'] == userid, ['ForUserId', 'Rating']]  # TODO: PostgreSQL
    idxs = req['ForUserId'].tolist()
    rats = req['Rating'].tolist()

    # rhe stands for "rating hot encoding"
    if dist == 'cosine':
        rhe = np.full((total,), -1)
    else:
        rhe = np.zeros((total,))
    rhe[idxs] = rats
    return rhe

def get_batch_info(userids, dist='cosine', total=220971):
    """
    Gets a matrix of rating-hot-vectors for a given list of user ids from a pool of items
    """
    batch_matrix = np.zeros((len(userids), total))
    for i, uid in enumerate(userids):
        batch_matrix[i] = _get_individual_info(uid, dist, total)
    return batch_matrix

def similarity_batch_individual(batch_userids, given_userid, dist='cosine', total=220971):
    """
    Computes a similarity between items chosen a batch of users and a user
    """
    mat = get_batch_info(batch_userids, dist, total)
    vec = _get_individual_info(given_userid, dist, total)
    sims = ssp.distance.cdist(mat, vec.reshape(1, -1), dist)
    return sims

def similarity_batch_batch(batch_userids, batch_given_userids, dist='cosine', total=220971):
    """
    Computes a similarity between items chosen by two batches of users
    """
    mat1 = get_batch_info(batch_userids, dist, total)
    mat2 = get_batch_info(batch_given_userids, dist, total)
    sims = ssp.distance.cdist(mat1, mat2, dist)
    return sims

def predict_individual(given_userid, given_itemid, dist='cosine', total=220971):
    """
    Predicts the value for a user-item pair
    """
    req_users = tr_data.loc[tr_data['ForUserId'] == given_itemid, ['UserId', 'Rating']]  # TODO: PostgreSQL
    userlist = req_users['UserId'].tolist()
    ratings = req_users['Rating'].tolist()
    req_sim = similarity_batch_individual(userlist, given_userid, dist, total).reshape(-1)
    return np.dot(ratings, req_sim) / req_sim.sum()

def predict_batch(given_userids, given_itemid, dist='cosine', total=220971):
    """
    Predicts the value for a list of pairs [(u1, i), (u2, i), (u3, i), ..., (un, i)]
    """
    req_users = tr_data.loc[tr_data['ForUserId'] == given_itemid, ['UserId', 'Rating']]  # TODO: PostgreSQL
    userlist = req_users['UserId'].tolist()
    ratings = np.array(req_users['Rating'].tolist())
    req_sim = similarity_batch_batch(userlist, given_userids, dist, total)
    denominator = req_sim.sum(0)
    denominator[denominator == 0.0] = 1e-12
    preds = ratings.dot(req_sim) / denominator
    full_bunch = np.hstack([np.array(given_userids).reshape(-1, 1),
                            np.full((len(given_userids), 1), given_itemid),
                            preds.reshape(-1, 1)])
    return full_bunch

def get_users_for_item(given_itemid):
    """
    Get a list of users paired with an item in the DB
    """
    return te_data.loc[te_data['ForUserId'] == given_itemid, 'UserId'].tolist()  # TODO: PostgreSQL


def get_predictions_per_thread(start, end):
    """
    Get Predictions per thread 
    """
    print("Started thread for Process {} ==> Thread range {} - {}".format(os.getpid(), start, end))
    unique_items = sorted_unique_items[start:end]
    for uitem in unique_items:
        te_users = get_users_for_item(uitem)
        batch_prediction = predict_batch(te_users, uitem)
        pd.DataFrame(data=batch_prediction, columns=['UserId', 'ForUserId', 'Rating']).to_csv('./FILES/item={}.csv'.format(uitem), index=False, header=False)
    print("Completed thread for Process {} ==> Thread range {} - {}".format(os.getpid(), start, end))

def spawn_threads(start, end):
    """
    Spawn no_of_thread threads and predict
    """
    batch_size = (end - start) / no_of_thread
    threads = []
    for x in range(no_of_thread):
        end_index = end if (start + batch_size > end) else start + batch_size
        threads.append(Thread(target=get_predictions_per_thread, args=((int)(start), (int)(end_index))))
        threads[-1].start()
        start += batch_size
    
    for x in threads:
        x.join()

def spawn_processes(batches):
    """
    Spawn process to later spawn threads
    """
    process = []
    for s, e in batches:
        process.append(Process(target=spawn_threads, args=(s, e)))
        process[-1].start()
    
    for p in process:
        p.join()

if __name__ == '__main__':

    tr_data = pd.read_csv('./data/train_user_ratings.csv', low_memory=False)
    te_data = pd.read_csv('./data/test_user_ratings.csv', low_memory=False)
    unique_items_count = len(list(set(te_data["ForUserId"])))
    sorted_unique_items = te_data.groupby(['ForUserId'])['UserId'].count().sort_values().index 

    batches = [(0,20000), (20000,36000), (36000,44000), (44000,60000), (60000,70000)]
    batches.extend([(i, i+5000) for i in range(70000,120001,5000)])

    batches = [(0,20000)]    #test
    spawn_processes(batches)
    print("done")
    
    batches.extend([(i, i+100) for i in range(120000,125001,100)])
    batches = [(i, i+100) for i in range(125000, unique_items_count, 50)]
    spawn_processes(batches)
