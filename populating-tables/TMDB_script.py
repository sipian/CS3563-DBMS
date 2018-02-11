import sys
import tmdbsimple as tmdb
import pandas as pd
import json

tmdb.API_KEY = '6b0c1e9b775e0a29bee614bd9086bf54'

data = pd.read_csv('title.basics.tsv', sep='\t', na_values='\\N', low_memory=False)

def get_data(imdb_id):
    obj = tmdb.base.TMDB()
    path = 'find/{}?api_key={}&external_source=imdb_id'.format(imdb_id, tmdb.API_KEY)
    return obj._GET(path=path)

cat = sys.argv[1]
ids = data[data.loc[:,'titleType'] == cat]['tconst'].values
del data

jsons = []

for cur_id in ids:
    try:
        key = 'movie_results' if cat == 'movie' else 'tv_results'
        inter = get_data(cur_id)[key]
    except Exception as e:
        print("At {}: {}".format(cur_id, e))
        continue

    try:
        if len(inter) == 0:
            continue

        if cat == 'movie':
            result = tmdb.Movies(inter[0]['id']).info()
            del result['belongs_to_collection']
            del result['video']
            del result['homepage']
            del result['tagline']
            for p in result['production_countries']:
                del p['iso_3166_1']
            for s in result['spoken_languages']:
                del s['iso_639_1']
        else:
            result = tmdb.TV(inter[0]['id']).info()
            del result['networks']
            del result['created_by']
            for s in result['seasons']:
                del s['poster_path']    

        del result['overview']
        del result['popularity']
        del result['poster_path']
        del result['backdrop_path']
        del result['id']
        for g in result['genres']:
            del g['id']

        jsons.append(result)
    except Exception as e:
        print("At {}: {}".format(cur_id, e))
        continue
    print('Done with {}'.format(cur_id))
    
re_data = pd.io.json.json_normalize(jsons)
re_data.to_csv('{}_data.tsv'.format(cat), sep='\t', na_rep='\\N')
