import time
import psycopg2
import numpy as np
from multiprocessing import Pool

conn = np.f
noOfThreads = 10
romfunction(lambda i: psycopg2.connect("dbname=friendship user=postgres password=postgres" ), (noOfThreads,), dtype=psycopg2.extensions.connection)



pool = mp.Pool(processes=4)
results = [pool.apply_async(cube, args=(x,)) for x in range(1,7)]
output = [p.get() for p in results]
print(output)


print(conn)
# cur = conn.cursor()

# normalized_mean queries
# cur.execute("select userid, AVG(rating) into user_average_ratings from final_ratings group by userid;")
# cur.execute("select final_ratings.userid, final_ratings.profileid, final_ratings.rating-user_average_ratings.avg from final_ratings INNER JOIN user_average_ratings on final_ratings.userid = user_average_ratings.userid;")