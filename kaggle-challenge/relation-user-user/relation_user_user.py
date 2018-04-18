import sys
import numpy as np
import pandas as pd
import threading

tr_data = pd.read_csv('./train_user_ratings.csv', low_memory=False)
te_data = pd.read_csv('./test_user_ratings.csv', low_memory=False)

item_information = None
user_information = None
item_links = {}
user_links = {}
vals = []

def get_users_for_item(itemid):
    return tr_data.loc[tr_data['ForUserId'] == itemid, ['UserId', 'Rating']]

def get_items_for_user(userid):
    return tr_data.loc[tr_data['UserId'] == userid, ['ForUserId', 'Rating']]

def get_details_for_items(itemid):
    usr_rat_mat = get_users_for_item(itemid)
    ratings = np.array(usr_rat_mat['Rating'].tolist())
    userids = np.array(usr_rat_mat['UserId'].tolist()).astype(int)
    vector = item_information[userids].values.astype(float)
    vector /= vector.sum()
    return ratings.dot(vector), vector.shape[0]

def get_details_for_users(userid):
    itm_rat_mat = get_items_for_user(userid)
    ratings = np.array(itm_rat_mat['Rating'].tolist())
    itemids = np.array(itm_rat_mat['ForUserId'].tolist()).astype(int)
    vector = user_information[itemids].values.astype(float)
    vector /= vector.sum()
    return ratings.dot(vector), vector.shape[0]

def get_user_item_information():
    print("Inside get_user_item_information")
    global item_information
    item_information = tr_data.groupby('UserId')['UserId'].count()
    global user_information
    user_information = tr_data.groupby('ForUserId')['UserId'].count()

def get_item_links():
    print("Starting item information gathering")
    unique_items = np.unique(te_data['ForUserId'].tolist())
    global item_links
    for iid in unique_items:
        avg_rat, cnt = get_details_for_items(iid)
        item_links[iid] = (avg_rat, cnt)
        if len(item_links) % 1000 == 0:
            print("1000-i")
    print("Done gathering item information")

def get_user_links():
    print("Starting user information gathering")
    unique_users = np.unique(te_data['UserId'].tolist())
    global user_links
    for uid in unique_users:
        avg_rat, cnt = get_details_for_users(uid)
        user_links[uid] = (avg_rat, cnt)
        if len(user_links) % 1000 == 0:
            print("1000-u")
    print("Done gathering user information")

def make_information_ready():
    print("Inside make information ready")
    get_user_item_information()

    t1 = threading.Thread(target=get_item_links)
    t2 = threading.Thread(target=get_user_links)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

def predict(target_type):
    global vals
    for tup in te_data.itertuples():
        u_l = user_links[tup[1]]
        i_l = item_links[tup[2]]
        rating = (u_l[0] * u_l[1] + i_l[0] * i_l[1]) / (u_l[1] + i_l[1])
        vals.append(rating)

    vals = np.array(vals).clip(min=1, max=10)
    if target_type == 'int':
        vals = np.around(vals, 0).astype(int)
    elif target_type == 'float':
        vals = np.around(vals, 5)

def get_results(target_type='int'):
    print("Information collecting....")
    make_information_ready()
    
    print("Start predicting....")
    predict(target_type)
    print("Done")

    np.savetxt(fname='relation-user-user.csv', X=vals, fmt='%d', header='Rating', comments='')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        get_results('int')
    else:
        get_results(sys.argv[1])
