import pandas as pd
import numpy as np

'''
List of all ignored categories (for now)
'''

actor_category = ["Actor", "Actress", "Actor in a Supporting Role", "Actress in a Supporting Role",
                  "Actor in a Leading Role", "Actress in a Leading Role","Directing (Comedy Picture)","Directing (Dramatic Picture)","Film Editing","Special Award"]
ignore_category = ["Art Direction"
                   , "Special Effects"
                   , "Art Direction (Black and White)"
                   , "Art Direction (Color)"
                   , "Music (Original Score)"
                   , "Music (Scoring)"
                   , "Music (Song)"
                   , "Documentary (Short Subject)"
                   , "Documentary"
                   , "Documentary (Feature)"
                   , "Music (Music Score of a Dramatic Picture)"
                   , "Music (Scoring of a Musical Picture)"
                   , "Music (Music Score of a Dramatic or Comedy Picture)"
                   , "Music (Music Score, Substantially Original)"
                   , "Sound Recording"
                   , "Outstanding Production"
                   , "Music (Scoring of Music, Adaptation or Treatment)"
                   , "Music (Original Music Score)"
                   , "Music (Original Score, for a Motion Picture [Not a Musical])"
                   , "Music (Score of a Musical Picture, Original or Adaptation)"
                   , "Music (Song, Original for the Picture)"
                   , "Music (Original Song Score)"
                   , "Music (Original Dramatic Score)"
                   , "Music (Scoring: Adaptation and Original Song Score)"
                   , "Music (Scoring: Original Song Score and Adaptation -Or- Scoring: Adaptation)"
                   , "Music (Original Song)"
                   , "Music (Original Song Score and Its Adaptation or Adaptation Score)"
                   , "Music (Original Song Score or Adaptation Score)"
                   , "Music (Original Musical or Comedy Score)"
                   , "Short Subject (Color)"
                   , "Short Subject (One Reel)"
                   , "Short Subject (Two Reel)"
                   , "Short Subject (Live Action)"
                   , "Unique and Artistic Picture {unsure about production company}"
                   , "Foreign Language Film"
                   , "Assistant Director"
                   , "Outstanding Production"
                   , "Unique and Artistic Picture"
                   , "Dance Direction"
                   , "Sound Recording"
                  ]



columnser = ['Year','Ceremony', 'Award', "Winner", "nconst", "tconst"]
columnsig= ['Year','Ceremony', 'Award', "Winner", "Name", "Film"]

x = pd.read_csv('database_toy.csv')
x['Winner']=x['Winner'].fillna(0.0)

y = pd.read_csv('name_basics.tsv',sep='\t')
z = pd.read_csv('title_basics.tsv',sep='\t')

new_df = pd.DataFrame(columns=columnser)
ignored_df = pd.DataFrame(columns=columnsig)
for index,rows in x.iterrows():
	print(type(rows))
	if rows['Award'] in ignore_category:
		ignored_df.append(rows,ignore_index=True)
		print(rows['Film'])
		new_row = pd.DataFrame.from_records([{'Year':rows.get('Year'),
						'Ceremony':rows.get('Ceremony'),
						'Award':rows.get('Award'),
						'Winner':rows.get('Winner'),
						'Name':rows.get('Name'),
						'Film':rows.get('Film')}])
		ignored_df = ignored_df.append(new_row,ignore_index=True)
		continue
	else:
		nconst = "null"
		tconst = "null"
		recipent = rows['Name']
		film = rows['Film']
		print(film)
		print(recipent)
		if rows['Award'] in actor_category:

			#yr  = rows['Year'].split('/')[0]
			index1 = z[z['primaryTitle'] == film]
			if index1.empty:
				tconst = np.nan
			else:	
			#index2 = index1[index1['startYear'] == yr]
				tconst = index1.iloc[0]['tconst']
			index1 = y[y['primaryName'] == recipent]
			if index1.empty:
				nconst = np.nan
			else:
			#index2 = index1.iloc[0]			
				nconst = index1.iloc[0]['nconst']			

			#tconst = z.iloc[z['primaryTitle'] == film]['tconst']
			new_row = pd.DataFrame.from_records([{'Year':rows.get('Year'),
						'Ceremony':rows.get('Ceremony'),
						'Award':rows.get('Award'),
						'Winner':rows.get('Winner'),
						'nconst':nconst,
						'tconst':tconst}])
			new_df = new_df.append(new_row,ignore_index=True)

			continue
		if film != "?" and ", " in  film:
			film = film.split(", ")
			num_rows = len(film)
			print(film)
			while num_rows > 0:

				
				index1 = z[z['primaryTitle'] == recipent]
				if index1.empty:
					tconst = np.nan
				else:				
				#index2 = index1[index1['startYear'] == yr]				
					tconst = index1.iloc[0]['tconst']
				
				index1 = y[y['primaryName'] == film[num_rows-1]]
				if index1.empty:
					nconst = np.nan
				else:
				#index2 = index1[tconst in index1['knownForTitles']]				
					index2 = index1.iloc[0]			
					nconst = index2['nconst']

				
#				nconst = y.iloc[y['primaryName'] == film[num_rows]]['nconst']
#				tconst = z.iloc[z['primaryTitle'] == recipent]['tconst']
				new_row = pd.DataFrame.from_records([{'Year':rows.get('Year'),
							'Ceremony':rows.get('Ceremony'),
							'Award':rows.get('Award'),
							'Winner':rows.get('Winner'),
							'nconst':nconst,
							'tconst':tconst}])
				new_df = new_df.append(new_row, ignore_index=True)
				num_rows -= 1
		else:
			index1 = z[z['primaryTitle'] == recipent]
			print(index1)
			if index1.empty:
				tconst = np.nan
			else:
			#index2 = index1[index1['startYear'] == yr]
			#index2 = index1.iloc[0]			
				tconst = index1.iloc[0].values[0]
			index1 = y[y['primaryName'] == film]
			if index1.empty:
				nconst = np.nan
			else:
			#index2 = index1[tconst in index1['knownForTitles']]				
				nconst = index1.iloc[0]['nconst']
#			nconst = y.iloc[y['primaryName'] == film]['nconst']
#			tconst = z.iloc[z['primaryTitle'] == recipent]['tconst']
			new_row = pd.DataFrame.from_records([{'Year':rows.get('Year'),
						'Ceremony':rows.get('Ceremony'),
						'Award':rows.get('Award'),
						'Winner':rows.get('Winner'),
						'nconst':nconst,
						'tconst':tconst}])
			new_df = new_df.append(new_row, ignore_index=True)


new_df = new_df.fillna("\\N")
new_df.to_csv('database_with_imdb.csv')
ignored_df.to_csv('database_with_ignored.csv')
