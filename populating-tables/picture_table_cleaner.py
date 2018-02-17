import pandas as pd

FULL_DB = 'title.basics_episode.tsv'
REQ_DB = 'title.basics_episode_required.csv'
EXT_DB = 'title.basics_episode_extra.csv'

# read the tsv excluding the fields
to_exclude = ['production_companies', 'production_countries',
              'spoken_languages', 'vote_average', 'vote_count', 'status']

# To get the column headers and perform a set difference
sample_db = pd.read_csv(FULL_DB, sep='\t', nrows=1)
to_include = list(set(sample_db.columns.tolist()) - set(to_exclude))
del sample_db
print(to_include)

# Now read the database entirely with required columns and save to different files based
# on titleType
cur_db = pd.read_csv(FULL_DB, sep='\t', na_values='\\N', usecols=to_include, low_memory=False)
cur_db.rename(columns={
                        'tconst': 'PictureID',
                        'primaryTitle': 'PrimaryTitle',
                        'OriginalTitle': 'ReleaseTitle',
                        'isAdult': 'Adult',
                        'startYear': 'StartYear',
                        'endYear': 'EndYear',
                        'runtimeMinutes': 'Duration',
                        'budget': 'Budget',
                        'original_language': 'Language',
                        'Revenue': 'GrossBoxOffice',
                        'seasonNumber': 'SeasonNumber',
                        'episodeNumber': 'EpisodeNumber',
                        'parentTconst': 'ParentPicture'
                     },
              inplace=True)
to_include = cur_db.columns.tolist()
print(to_include)

to_include.remove('titleType')  # this is inplace
req_db = cur_db[(cur_db['titleType'] == 'movie') |
                (cur_db['titleType'] == 'tvSeries') |
                (cur_db['titleType'] == 'tvEpisode')]
req_db.to_csv(REQ_DB, sep=',', na_rep='\\N', columns=to_include, index=False)
ext_db = cur_db[(cur_db['titleType'] != 'movie') &
                (cur_db['titleType'] != 'tvSeries') &
                (cur_db['titleType'] != 'tvEpisode')]
ext_db.to_csv(EXT_DB, sep=',', na_rep='\\N', columns=to_include, index=False)

# Remove from RAM
del cur_db
del ext_db

# Get list of valid tconsts for role table generation. This uses only req_db
tconst_list = req_db['PictureID'].tolist()
tconst_file = open('PictureID_list.txt', 'w')
for ID in tconst_list:
    tconst_file.write('{}\n'.format(ID))
tconst_file.close()
