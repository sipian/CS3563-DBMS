import pandas as pd

tr_data = pd.read_csv('train_user_ratings.csv', low_memory=False)
te_data = pd.read_csv('test_user_ratings.csv', low_memory=False)

usr_avg = tr_data.groupby(['UserId'])['Rating'].mean()
itm_avg = tr_data.groupby(['ForUserId'])['Rating'].mean()
del tr_data

f1 = open('user_averaging.csv', 'w')
f1.write('Rating\n')

for tup in te_data.itertuples():
    f1.write('{}\n'.format(round(usr_avg[tup[1]], 7)))

f1.close()

f2 = open('user-item_averaging.csv', 'w')
f2.write('Rating\n')

for tup in te_data.itertuples():
    full_rat = usr_avg[tup[1]]
    try:
        full_rat += itm_avg[tup[2]]
        full_rat /= 2
    except:
        pass
    f2.write('{}\n'.format(round(full_rat, 7)))
