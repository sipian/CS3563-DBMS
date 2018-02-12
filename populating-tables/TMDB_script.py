import sys
import tmdbsimple as tmdb
import pandas as pd
import numpy as np
import json
import signal

cat = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])
tmdb.API_KEY = sys.argv[4]

def get_data(imdb_id):
    obj = tmdb.base.TMDB()
    path = 'find/{}?api_key={}&external_source=imdb_id'.format(imdb_id, tmdb.API_KEY)
    return obj._GET(path=path)

ids = np.genfromtxt('IMDB-ID_{}_list'.format(cat), dtype=str).tolist()

jsons = []

for cur_id in ids[start:end]:
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

    if len(jsons) % 100 == 0:
        print("Autosave....")
        re_data = pd.io.json.json_normalize(jsons)
        re_data.to_csv('{}_data_{}_{}.tsv'.format(cat, start, end), sep='\t', na_rep='\\N')

re_data = pd.io.json.json_normalize(jsons)
re_data.to_csv('{}_data_{}_{}.tsv'.format(cat, start, end), sep='\t', na_rep='\\N')
