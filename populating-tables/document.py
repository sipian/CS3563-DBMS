import ast
import pandas as pd

def func(arr):
	# print ("Inside new")
	if arr=="genres_y" or arr=="production_companies" or arr=="production_countries" or  arr=="spoken_languages":
		# print ("Inside 1st if")
		return arr
	else:
		# print ("Inside 1st else ", arr)
		try:
			xy = ast.literal_eval(arr)
		except ValueError:
			return []
		else:
			# print ("Inside 1st else after literal_eval ", type(xy))
			if type(xy) != type([]) or len(xy)==0:
				# print ("Inside 2nd if")
				return []
			else:
				# print ("Inside 2nd else")
				return [x['name'] for x in xy]


#dj = pd.read_csv("./combined.csv", sep='\t', na_values="\\N", low_memory=False)

imdb = pd.read_csv("./imdb/title.basics.tsv", sep='\t', na_values="\\N", low_memory=False)
tsdb = pd.read_csv("./the-movies-dataset/movies_metadata.csv", sep=',', na_values="", low_memory=False, names=['adult','belongs_to_collection','budget','genres','homepage','id','imdb_id','original_language','original_title','overview','popularity','poster_path','production_companies','production_countries','release_date','revenue','runtime','spoken_languages','status','tagline','title','video','vote_average','vote_count'])

dropped_tsdb = tsdb.drop(columns=["adult","belongs_to_collection","id","original_title","poster_path","release_date","runtime","title","tagline","video"])
dropped_tsdb = dropped_tsdb.rename(columns = {'imdb_id':'tconst'})

ans = pd.merge(imdb,dropped_tsdb,on='tconst',how='left')
ans['genres_y'] = ans['genres_y'].apply(func)
ans['production_companies'] = ans['production_companies'].apply(func)
ans['production_countries'] = ans['production_countries'].apply(func)
ans['spoken_languages'] = ans['spoken_languages'].apply(func)
ans.to_csv('./combined.csv',sep='\t',na_rep='\\N')
ans.isnull().sum()


# Count of null for movies attributes

# tconst                        0
# titleType                     0
# primaryTitle                  4
# originalTitle               180
# isAdult                       0
# startYear                272322
# endYear                 4709937
# runtimeMinutes          3291283
# genres                   388992
# budget                  4700832
# homepage                4738490
# original_language       4700843
# overview                4701784
# popularity              4700835
# production_companies    4700835
# production_countries    4700835
# revenue                 4700835
# spoken_languages        4700835
# status                  4700916
# vote_average            4700835
# vote_count              4700835
# dtype: int64
# 4746236