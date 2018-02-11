import pandas as pd

dj = pd.read_csv("./combined.csv", sep='\t', na_values="\\N", low_memory=False)

imdb = pd.read_csv("./imdb/title.basics.tsv", sep='\t', na_values="\\N", low_memory=False)

tsdb = pd.read_csv("./the-movies-dataset/movies_metadata.csv", sep=',', na_values="", low_memory=False, names=['adult','belongs_to_collection','budget','genres','homepage','id','imdb_id','original_language','original_title','overview','popularity','poster_path','production_companies','production_countries','release_date','revenue','runtime','spoken_languages','status','tagline','title','video','vote_average','vote_count'])


dropped_tsdb = tsdb.drop(columns=["adult","belongs_to_collection","genres","id","original_title","poster_path","release_date","runtime","title","tagline","video"])

dropped_tsdb = dropped_tsdb.rename(columns = {'imdb_id':'tconst'})

ans = pd.merge(imdb,dropped_tsdb,on='tconst',how='left')

ans.isnull().sum()

ans.columns.values

ans.to_csv('./combined.csv',sep='\t',na_rep='\\N')

tsdb.isnull().sum()



[{'id': 16, 'name': 'Animation'}, {'id': 35, 'name': 'Comedy'}, {'id': 10751, 'name': 'Family'}]


import ast
import pandas as pd
tsdb = pd.read_csv("./the-movies-dataset/movies_metadata.csv", sep=',', na_values="", low_memory=False, names=['adult','belongs_to_collection','budget','genres','homepage','id','imdb_id','original_language','original_title','overview','popularity','poster_path','production_companies','production_countries','release_date','revenue','runtime','spoken_languages','status','tagline','title','video','vote_average','vote_count'])
def func(arr):
	if arr == "genres":
		return arr
	else:
		xy = ast.literal_eval(arr)
		if len(xy) == 0:
			return xy
		else:
			return [x['name'] for x in xy]

tsdb['genres'] = tsdb['genres'].apply(func)


Count of null for movies attributes

tconst                        0
titleType                     0
primaryTitle                  4
originalTitle               180
isAdult                       0
startYear                272322
endYear                 4709937
runtimeMinutes          3291283
genres                   388992
budget                  4700832
homepage                4738490
original_language       4700843
overview                4701784
popularity              4700835
production_companies    4700835
production_countries    4700835
revenue                 4700835
spoken_languages        4700835
status                  4700916
vote_average            4700835
vote_count              4700835
dtype: int64


4746236