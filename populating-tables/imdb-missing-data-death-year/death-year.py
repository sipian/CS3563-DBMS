#dth_year_regex = re.compile("<th scope=\"row\">Died</th>\\\\n<td>{}{}{}{}{}".format(month,separator,date,separator,year))

import re
import sys
import urllib
import numpy as np
import pandas as pd 


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def check_regex (regex, string):
	print((bool)(re.match(regex, string)))
	sys.exit(0)

def check(wiki, regex):
	page = urllib.request.urlopen(wiki)
	page = str(page.read())
	x = regex.findall(page)
	if len(x) != 0:
		print("Death year of ",name," :: ",x[-1])
	else:
		print("fail")
	sys.exit(0)



month = "(January|February|March|April|May|June|July|August|September|October|November|December)"
year = "([0-9]{4})"
date = "([0-9]{1,2})"
separator = "(,|;|\s|&#160;)+"
middlebar = "(–|-|\\\\xe2\\\\x80\\\\x93)+"

re.DOTALL
dth_year_regex_1 = re.compile("\\({}{}{}{}{}{}{}{}{}{}{}{}{}\\)".format(month,separator,date,separator,year,separator,middlebar,separator,month,separator,date,separator,year))
dth_year_regex_2 = re.compile("\\({}{}{}{}{}{}{}{}{}{}{}{}{}\\)".format(month,separator,date,separator,year,separator,middlebar,separator,date,separator,month,separator,year))
dth_year_regex_3 = re.compile("\\({}{}{}{}{}{}{}{}{}{}{}{}{}\\)".format(date,separator,month,separator,year,separator,middlebar,separator,month,separator,date,separator,year))
dth_year_regex_4 = re.compile("\\({}{}{}{}{}{}{}{}{}{}{}{}{}\\)".format(date,separator,month,separator,year,separator,middlebar,separator,date,separator,month,separator,year))

#born May 2, 1972
born_year_1 = re.compile(".*(born){}{}{}{}{}{}".format(separator,month,separator,date,separator,year))
born_year_2 = re.compile(".*born{}{}{}{}{}{}".format(separator,date,separator,month,separator,year))


res = []

chunksize = 10**4

output_file = open("testfile.csv", "ab")

for data in pd.read_csv("~/btech/sem 6/dbms-2/project-dataset/name.basics.tsv", skiprows=30, chunksize=chunksize, delimiter='\t'):
	col = np.array(data)
	# np.savetxt(output_file,col,fmt="%s",delimiter="\t")
	
	for i, name in enumerate(col[:,1]):

		if isEnglish(name) == False:
			continue


		if col[i][2] != "\\N" and col[i][3] != "\\N":
			continue

		wiki = "https://en.wikipedia.org/wiki/"+ name.replace(" ", "_")
		print(wiki)
		try:
			page = urllib.request.urlopen(wiki)
		except urllib.error.HTTPError as e:
			if e.code == 404:
				print("Page 404 error\n")
			else:
				print("Page error\n", e)
		except urllib.error.URLError as e:
			print("Not an HTTP-specific error (e.g. connection refused)")
		else:
			# 200
			soup_string = str(page.read())

			#birth and death
			print ("checking 1st")
			x = dth_year_regex_1.findall(soup_string)
			if len(x) != 0:
				print("Death year of ",name," :: ",x[-1])
				continue

			print ("checking 2nd")
			x = dth_year_regex_2.findall(soup_string)
			if len(x) != 0:
				print("Death year of ",name," :: ",x[-1])
				continue

			print ("checking 3rd")
			x = dth_year_regex_3.findall(soup_string)
			if len(x) != 0:
				print("Death year of ",name," :: ",x[-1])
				continue

			print ("checking 4th")
			x = dth_year_regex_4.findall(soup_string)
			if len(x) != 0:
				print("Death year of ",name," :: ",x[-1])
				continue

			if col[i][2] != "\\N":
				continue

			if (wiki == "https://en.wikipedia.org/wiki/Alan_Miller" or 
			   wiki == "https://en.wikipedia.org/wiki/Henner_Hofmann"):
				continue

			sys.exit(0)
			# x = born_year_1.findall(soup_string)
			# print(x)
			# if len(x) != 0:
			# 	print("Death year of ",name," :: ",x[-1])
			# 	continue

			# x = born_year_2.findall(soup_string)
			# if len(x) != 0:
			# 	print("Death year of ",name," :: ",x[-1])
			# 	continue



  #   	page = urllib.request.urlopen(wiki)
  #   	soup = BeautifulSoup(page,  "lxml")
  #   	right_table=soup.find_all('table', class_='infobox biography vcard')
  #   	print(name.replace(" ", "_") , " -- " , len(right_table))
  #   	sys.stdout.flush()
  #   	if not right_table:
  #   		print (wiki , " is 404")
  #   		sys.stdout.flush()