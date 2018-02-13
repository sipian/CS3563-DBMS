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

def fill_missing_values(x):
	x["budget"] = x["budget"].replace("0","\\N")
	x["budget"] = x["budget"].fillna("\\N")
	x["original_language"] = x["original_language"].fillna("\\N")
	x["production_companies"] = x["production_companies"].replace("[]","\\N")
	x["production_companies"] = x["production_companies"].fillna("\\N")
	x["production_countries"] = x["production_countries"].replace("[]","\\N")
	x["production_countries"] = x["production_countries"].fillna("\\N")
	x["revenue"] = x["revenue"].replace("0","\\N")
	x["revenue"] = x["revenue"].fillna("\\N")
	x["spoken_languages"] = x["spoken_languages"].replace("[]","\\N")
	x["spoken_languages"] = x["spoken_languages"].fillna("\\N")
	x["status"] = x["status"].fillna("\\N")
	x["vote_average"] = x["vote_average"].fillna("\\N")
	x["vote_count"] = x["vote_count"].fillna("\\N")
	return x



imdb = pd.read_csv("./imdb/title.basics.tsv", sep='\t', na_values="\\N", low_memory=False)

movies_dataset_tsdb = pd.read_csv("./the-movies-dataset/movies_metadata.csv", sep=',', na_values="", low_memory=False, names=['adult','belongs_to_collection','budget','genres','homepage','id','imdb_id','original_language','original_title','overview','popularity','poster_path','production_companies','production_countries','release_date','revenue','runtime','spoken_languages','status','tagline','title','video','vote_average','vote_count'])
movies_dataset_tsdb = movies_dataset_tsdb.drop(columns=['adult','belongs_to_collection','genres','homepage','id','original_title','overview','popularity','poster_path','release_date','runtime','tagline','title','video'])
movies_dataset_tsdb = movies_dataset_tsdb.rename(columns = {'imdb_id':'tconst'})

vishwak_dataset_1 = pd.read_csv("./drive-download-20180213T073845Z-001/movie_data_0_20000.tsv", sep='\t', low_memory=False, names=['adult','budget','genres','imdb_id','original_language','original_title','production_companies','production_countries','release_date','revenue','runtime','spoken_languages','status','title','vote_average','vote_count'])
vishwak_dataset_1 = vishwak_dataset_1.drop(columns=['adult','genres','original_title','release_date','runtime','title'])
vishwak_dataset_1 = vishwak_dataset_1.rename(columns = {'imdb_id':'tconst'})

vishwak_dataset_2 = pd.read_csv("./drive-download-20180213T073845Z-001/movie_data_20000_40000.tsv", sep='\t', low_memory=False, names=['adult','budget','genres','imdb_id','original_language','original_title','production_companies','production_countries','release_date','revenue','runtime','spoken_languages','status','title','vote_average','vote_count'])
vishwak_dataset_2 = vishwak_dataset_2.drop(columns=['adult','genres','original_title','release_date','runtime','title'])
vishwak_dataset_2 = vishwak_dataset_2.rename(columns = {'imdb_id':'tconst'})

vishwak_dataset_3 = pd.read_csv("./drive-download-20180213T073845Z-001/movie_data_200000_300000.tsv", sep='\t', low_memory=False, names=['adult','budget','genres','imdb_id','original_language','original_title','production_companies','production_countries','release_date','revenue','runtime','spoken_languages','status','title','vote_average','vote_count'])
vishwak_dataset_3 = vishwak_dataset_3.drop(columns=['adult','genres','original_title','release_date','runtime','title'])
vishwak_dataset_3 = vishwak_dataset_3.rename(columns = {'imdb_id':'tconst'})

vishwak_dataset_4 = pd.read_csv("./drive-download-20180213T073845Z-001/movie_data_300000_435042.tsv", sep='\t', low_memory=False, names=['adult','budget','genres','imdb_id','original_language','original_title','production_companies','production_countries','release_date','revenue','runtime','spoken_languages','status','title','vote_average','vote_count'])
vishwak_dataset_4 = vishwak_dataset_4.drop(columns=['adult','genres','original_title','release_date','runtime','title'])
vishwak_dataset_4 = vishwak_dataset_4.rename(columns = {'imdb_id':'tconst'})


movies_dataset_tsdb["budget"] = movies_dataset_tsdb["budget"].replace("0","\\N")
movies_dataset_tsdb["budget"] = movies_dataset_tsdb["budget"].fillna("\\N")
movies_dataset_tsdb["production_companies"] = movies_dataset_tsdb["production_companies"].replace("[]","\\N")
movies_dataset_tsdb["production_companies"] = movies_dataset_tsdb["production_companies"].fillna("\\N")
movies_dataset_tsdb["production_countries"] = movies_dataset_tsdb["production_countries"].replace("[]","\\N")
movies_dataset_tsdb["production_countries"] = movies_dataset_tsdb["production_countries"].fillna("\\N")
movies_dataset_tsdb["revenue"] = movies_dataset_tsdb["revenue"].replace("0","\\N")
movies_dataset_tsdb["revenue"] = movies_dataset_tsdb["revenue"].fillna("\\N")
movies_dataset_tsdb["spoken_languages"] = movies_dataset_tsdb["spoken_languages"].replace("[]","\\N")
movies_dataset_tsdb["spoken_languages"] = movies_dataset_tsdb["spoken_languages"].fillna("\\N")
movies_dataset_tsdb["status"] = movies_dataset_tsdb["status"].fillna("\\N")
movies_dataset_tsdb["vote_average"] = movies_dataset_tsdb["vote_average"].fillna("\\N")
movies_dataset_tsdb["vote_count"] = movies_dataset_tsdb["vote_count"].fillna("\\N")


vishwak_dataset_1 = fill_missing_values(vishwak_dataset_1)
vishwak_dataset_2 = fill_missing_values(vishwak_dataset_2)
vishwak_dataset_3 = fill_missing_values(vishwak_dataset_3)
vishwak_dataset_4 = fill_missing_values(vishwak_dataset_4)

combined_csv = vishwak_dataset_1.append(vishwak_dataset_2)
combined_csv = combined_csv.append(vishwak_dataset_3)
combined_csv = combined_csv.append(vishwak_dataset_4)
combined_csv.to_csv('./drive-download-20180213T073845Z-001/combined.csv',sep='\t',na_rep='\\N')

combined_csv = pd.read_csv("./drive-download-20180213T073845Z-001/combined.csv", sep='\t', low_memory=False, names=['budget','tconst','original_language','production_companies','production_countries','revenue','spoken_languages','status','vote_average','vote_count'])
movies_dataset_tsdb = pd.read_csv("./drive-download-20180213T073845Z-001/dropped_imdb_nan_tmdb.csv", sep='\t', low_memory=False, names=['budget','tconst','original_language','production_companies','production_countries','revenue','spoken_languages','status','vote_average','vote_count'])
final = pd.read_csv("./drive-download-20180213T073845Z-001/final.csv", sep='\t', low_memory=False, names=['budget','tconst','original_language','production_companies','production_countries','revenue','spoken_languages','status','vote_average','vote_count'])



# movies_dataset_tsdb["original_language"].loc[movies_dataset_tsdb["original_language"] == "\\N"]
# x = combined_csv.duplicated(subset="tconst")
# movies_dataset_tsdb.loc[x == True]
# final = final[x == True]


ans = pd.merge(imdb,dropped_tsdb,on='tconst',how='left')
ans['genres_y'] = ans['genres_y'].apply(func)
ans['production_companies'] = ans['production_companies'].apply(func)
ans['production_countries'] = ans['production_countries'].apply(func)
ans['spoken_languages'] = ans['spoken_languages'].apply(func)
ans.to_csv('./combined.csv',sep='\t',na_rep='\\N', index=False)
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