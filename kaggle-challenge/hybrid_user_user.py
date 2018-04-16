import pandas as pd
import numpy as np

tr_data = pd.read_csv('../train_user_ratings.csv', low_memory=False)
te_data = pd.read_csv('../test_user_ratings.csv', low_memory=False)

user_information = None
final_ratings = None

def get_users_for_item(itemid):
    return tr_data.loc[tr_data['ForUserId'] == itemid, ['UserId', 'Rating']]

def get_details_for_users(itemid):
    usr_rat_mat = get_users_for_item(itemid)
    ratings = np.array(usr_rat_mat['Rating'].tolist())
    userids = np.array(usr_rat_mat['UserId'].tolist()).astype(int)
    vector = user_information[userids].values.astype(float)
    vector /= vector.sum()
    return ratings.dot(vector)

def get_user_information():
    global user_information
    user_information = tr_data.groupby('UserId')['UserId'].count()

def predict():
    unique_items = np.unique(te_data['ForUserId'].tolist())
    vals = []

    for i, u in enumerate(unique_items):
        vals.append(get_details_for_users(u))
    vals = np.array(vals).clip(min=1, max=10)
    vals = np.around(vals, 0).astype(int)

    global final_ratings
    final_ratings = np.hstack([unique_items.reshape(-1, 1), vals.reshape(-1, 1)])

def get_results():
    print("Obtaining user info")
    get_user_information()
    print("Start predicting")
    predict()

    final = te_data.merge(pd.DataFrame(final_ratings, columns=['ForUserId', 'Rating']),
                          how='left', on=['ForUserId'])
    final['Rating'].to_csv('user-user-hybrid.csv', index=False, header='Rating')

if __name__ == '__main__':
    get_results()
