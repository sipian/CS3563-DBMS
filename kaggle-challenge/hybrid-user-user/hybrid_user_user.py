import sys
import csv
import time
import psycopg2
import numpy as np
import pandas as pd

start = time.time()

GROUP_ID = "group2"

conn = psycopg2.connect("dbname=friendship user=postgres password=postgres")
cur = conn.cursor()

# creating and filling in the tables
cur.execute("DROP TABLE IF EXISTS Ratings;")
cur.execute("CREATE TABLE Ratings ( UserID integer, ProfileID integer,  Rating integer);")
cur.execute("CREATE TABLE IF NOT EXISTS Gender (  UserID integer primary key, Gender char(1));")
# for now, ratings is filled as from the training data
print("Write to database")
cur.execute("COPY Ratings FROM 'train_user_ratings.csv' CSV delimiter ',' NULL '\\N' ENCODING 'unicode' header;")

print("Fetching from database")
cur.execute("SELECT *  FROM Ratings")
rows = cur.fetchall()

np_test_data = np.array([list(elem) for elem in rows])
tr_data = pd.DataFrame(data = np_test_data, columns=["UserId","ForUserId","Rating"]) 
del np_test_data, rows   #free memory

te_data = pd.read_csv('test_user_ratings.csv', low_memory=False)

print("Created Dataframes")

conn.commit()
cur.close()
conn.close()

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
    final['Rating'].to_csv('hybrid-output-{}.csv'.format(GROUP_ID), index=False, header='Rating')

if __name__ == '__main__':
    get_results()
    end = time.time()

    with open('time.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([GROUP_ID, str(end - start)])


