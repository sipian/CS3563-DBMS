import psycopg2
import numpy as np
import pandas as pd
import multiprocessing as mp

no_of_process = 4
test_data = pd.read_csv("./data/test_user_ratings.csv")
unique_items = np.array(list(set(test_data["ForUserId"])))

def _get_individual_info(userid, cur, total=220969):
    """
    Gets a rating-hot-vector for a given user id from a pool of items
    """
    # Assume the data frame is in Pandas for now, named "cur_db"

    # req = cur_db.loc[cur_db['UserId'] == userid, ['ForUserId', 'Rating']]
    # idxs = req['ForUserId'].tolist()
    # rats = req['Rating'].tolist()

    cur.execute("SELECT ProfileID, Rating FROM ratings WHERE userid = "+str(userid)+";")
    rows = cur.fetchall()
    rows = np.array([list(i) for i in rows])
    idxs = rows[:,1]
    rats = rows[:,2]

    # rhe stands for "rating hot encoding"
    rhe = np.zeros((total,))
    rhe[idxs] = rats
    return rhe

def get_batch_info(userids, cur, total=220969):
    """
    Gets a matrix of rating-hot-vectors for a given list of user ids from a pool of items
    """
    batch_matrix = np.zeros((len(userids), total))
    for i, uid in enumerate(userids):
        batch_matrix[i] = _get_individual_info(uid, cur, total)
    return batch_matrix

def jobHandler(i, total=220969):
    global noOfProcess
    conn = psycopg2.connect("dbname=friendship user=postgres password=postgres")
    curr = conn.cursor()
    batch_size = total/noOfProcess

    start_index = (int)(i*batch_size + 1)

    if i == noOfProcess-1:
        end_index = total + 1
    else:
        end_index = (i+1)*batch_size + 1
    end_index = (int)(end_index)

    print("Process {} : {} - {}".format(i, start_index, end_index))
    userids = np.arange(start_index, end_index)
    return get_batch_info(userids , curr)


pool = mp.Pool(processes=noOfProcess)
results = [pool.apply(handleProcess, args=(i,)) for i in range(0,noOfProcess)]

output = [p.get() for p in results]
print(output.size())

# normalized_mean queries
# cur.execute("select userid, AVG(rating) into user_average_ratings from final_ratings group by userid;")
# cur.execute("select final_ratings.userid, final_ratings.profileid, final_ratings.rating-user_average_ratings.avg from final_ratings INNER JOIN user_average_ratings on final_ratings.userid = user_average_ratings.userid;")