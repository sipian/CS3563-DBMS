import pandas as pd 
import urllib
from bs4 import BeautifulSoup
import sys
import numpy as np


month = "(January|February|March|April|May|June|July|August|September|October|November|December)"
year = "([0-9]{4})"
date = "([0-9]{2})"
separator = "(\\,|\s|\\&\\#160\\;)+"
middlebar = "(\\–)+"


dth_year_regex = "{}{}{}{}{}{}{}{}{}{}{}{}{}".format(month,separator,date,separator,year,separator,middlebar,separator,month,separator,date,separator,year)

import re
wiki = "https://en.wikipedia.org/wiki/Fred_Astaire"
# input("Enter")

try:
	page = urllib.request.urlopen(wiki)
except urllib.error.HTTPError as e:
    if e.code == 404:
        print("Page 404 error")
    else:
        print("Page Error :: ", e)
except urllib.error.URLError as e:
    print("Not an HTTP-specific error (e.g. connection refused)")
else:
    # 200
	soup_string = str(page.read())
	open("./val.txt", "w").write(soup_string)
	print ((bool)(re.match("Fred_Astaire", soup_string)))
	# print("test :: ", len(soup.find_all("Fred")))
	# for tag in soup.find_all(re.compile("Fred")):
	#     print("tag.name :: ", tag.name)
	#     print("tag :: ", tag)



# chunksize = 10**4

# for data in pd.read_csv("~/btech/sem 6/dbms-2/project-dataset/name.basics.tsv", chunksize=chunksize, delimiter='\t'):
#     col = np.array(data)
#     print ("next iteration")
#     for i, name in enumerate(col[:,1]):
#     	wiki = "https://en.wikipedia.org/wiki/"+ name.replace(" ", "_")
#     	page = urllib.request.urlopen(wiki)
#     	soup = BeautifulSoup(page,  "lxml")
#     	right_table=soup.find_all('table', class_='infobox biography vcard')
#     	print(name.replace(" ", "_") , " -- " , len(right_table))
#     	sys.stdout.flush()
#     	if not right_table:
#     		print (wiki , " is 404")
#     		sys.stdout.flush()