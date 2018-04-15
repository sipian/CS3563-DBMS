import psycopg2
import time
conn = psycopg2.connect("dbname=friendship user=postgres password=Sahil23!" )
cur = conn.cursor()

# normalized_mean queries
# cur.execute("select userid, AVG(rating) into user_average_ratings from final_ratings group by userid;")
# cur.execute("select final_ratings.userid, final_ratings.profileid, final_ratings.rating-user_average_ratings.avg from final_ratings INNER JOIN user_average_ratings on final_ratings.userid = user_average_ratings.userid;")

test_userID = 23408
test_profileID = 38551
start = time.time()
cost = 0
arg_cost = 0
for i in range(1,135359):
    if i != test_userID:
        cur.execute("WITH a_table AS (select * from norm_ratings where userid =" + str(test_userID) + "),b_table AS (select * from norm_ratings where userid = " + str(i) + ")SELECT SUM(a_table.normalized_mean*b_table.normalized_mean)/(SQRT(SUM(a_table.normalized_mean*a_table.normalized_mean))*SQRT(SUM(b_table.normalized_mean*b_table.normalized_mean))) FROM a_table,b_table WHERE a_table.ProfileID = b_table.ProfileID;")
        rows = cur.fetchall()
        print(rows)
        if rows[0][0] == None:
            x = 0
        else:
            x = rows[0][0]
        if i != test_profileID
            cur.execute("select rating from final_ratings where userid = "+str(i)+" and profileid = "+str(test_profileID)+";")
            rows = cur.fetchall()
            print(rows)
            if not rows:
                y = 0
            else:
                y = rows[0][0]
            cost += x*y
            arg_cost += x
conn.commit()
end = time.time()
print(cost, arg_cost)
print(rows[0][0])
print(str(end-start))