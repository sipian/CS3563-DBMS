import psycopg2

conn = psycopg2.connect("dbname=friendship user=postgres password=postgres")

cur = conn.cursor()

#creating and filling in the tables
cur.execute("CREATE TABLE Ratings (	UserID integer,	ProfileID integer,	Rating integer);")
cur.execute("CREATE TABLE Gender (	UserID integer primary key,	Gender char(1));")

# for now, ratings is filled as from the training data
cur.execute("COPY Ratings FROM '/tmp/train_user_ratings.csv' CSV delimiter ',' NULL '\\N' ENCODING 'unicode' header;")
cur.execute("COPY Gender FROM '/tmp/gender.csv' CSV delimiter ',' NULL '\\N' ENCODING 'unicode' header;")

conn.commit()
cur.close()
conn.close()



