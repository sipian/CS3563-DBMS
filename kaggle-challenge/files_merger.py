import psycopg2
import os

conn = psycopg2.connect("dbname=friendship1 user=postgres password=Sahil23!" )
cur = conn.cursor()

path_to_merged_file = ""
test_dataset_filename = ""
result_pathname = ""

os.system(" cat item* >> result.csv")
os.system(" echo \"UserId,ForUserId,Rating\" > result_header.csv")
os.system("cat result_header.csv result.csv >> final_result.csv")

print("Done with concatenation")

cur.execute("CREATE TABLE Test_Ratings (	UserID integer,	ProfileID integer);")
cur.execute("COPY Test_Ratings FROM '" + test_dataset_filename + "' CSV delimiter ',' NULL '\\N' ENCODING 'unicode' header;")

cur.execute("CREATE TABLE Merged_Test_Ratings (UserID integer,	ForUserID integer, Rating Integer);")
cur.execute("COPY Merged_Test_Ratings FROM '" + path_to_merged_file + "' CSV delimiter ',' NULL '\\N' ENCODING 'unicode' header;")

cur.execute("SELECT Merged_Test_Ratings INTO final_ratings FROM Test_Ratings INNER JOIN Merged_Test_Ratings ON Test_Ratings.userid = Merged_Test_Ratings.userid;")
cur.execute("COPY final_ratings to " + result_pathname + " CSV DELIMITER \',\' ")
conn.commit()
cur.close()
conn.close()