# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:15:39 2020

@author: akshat
"""

import sqlite3
import pandas as pd
from collections import Counter
import ast
import itertools


pd.set_option('display.max_columns',40)

conn = sqlite3.connect('all_spotify.db')
c = conn.cursor()
df = pd.read_sql_query("select * from spotify;", conn)

df.columns

col=list(df.columns)

'''
col=['row_counter', 'song_id', 'song_name', 'artist_id', 'artist_name',
       'album_id', 'explicit', 'disc_number', 'track_number', 'album_name',
       'uri', 'tempo', 'type', 'key', 'loudness', 'mode', 'speechiness',
       'liveness', 'valence', 'danceability', 'energy', 'track_href',
       'analysis_url', 'duration_ms', 'time_signature', 'acousticness',
       'instrumentalness', 'artist_genres', 'artist_popularity',
       'album_genres', 'album_popularity', 'album_release_date',
       'sp_album_release_date_year']
'''

#creating copy of orignal data
#asd=df.copy()

#1. Remove songs with non english characters 

#asd.sort_values(by=['song_name'],inplace=True)
#asd.reset_index(drop=True,inplace=True)

#asd['song_name'][1537605:1573145]

# from index 1537417 onwards all 99% of songs are not english
# checking again just for non-english language
#test=asd[1537418:1573144].copy()

#asd1=asd[0:1537417].copy()
#asd1=asd.copy()

# total records removed till now are 35727

#len(asd)-len(asd1)

asd2=df.copy()
#2. Remove duplicates of Song-name and artist
lst1=['song_name', 'artist_id']



asd2.drop_duplicates(subset=lst1,keep='last',inplace=True)


# Additional records removed are - 190982
len(asd1)-len(asd2)

# diff is 194127

cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

con = sqlite3.connect('spotify.db')
asd2.to_sql("spotify", con, schema=None, if_exists='fail', index=False, index_label=col, chunksize=None, dtype=None)


'''
big =['artist_id','tempo', 'type', 'key', 'loudness', 'mode', 'speechiness','liveness', 'valence', 'danceability', 'energy','duration_ms','acousticness',
       'instrumentalness']
asd2.groupby(by=big).count()

'''

df1 = pd.read_sql_query("select * from spotify;", con)

len(df)-len(df1)
# verify diff is 194127

cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

df1.columns


#genres=[]
#genres=[ast.literal_eval(i) for i in asd['artist_genres']]
#flat_list = [item for sublist in genres for item in sublist]


#################Creating raw file for network and edges among music genre

flat_list = [item for i in asd2['artist_genres'] for item in ast.literal_eval(i)]
len(flat_list)

unique1=list(set(flat_list))
len(unique1)
d=dict(Counter(flat_list))
#Sorting dictionary
d={k: v for k, v in sorted(d.items(), key=lambda item: item[1],reverse=True)}

with open('genres.csv', 'w') as f:
    for key in d.keys():
        f.write("%s,%s\n"%(key,d[key]))
        

new_list = [ ast.literal_eval(i) for i in asd2['artist_genres']]
fd=[list(itertools.combinations(i,2)) for i in new_list if i!=[]]
flat_list2 = [item for i in fd for item in i]
 
df4=pd.DataFrame()
df5=pd.DataFrame()

df4['source']=[i for i,j in flat_list2]
df4['target']=[j for i,j in flat_list2]

df5['source']=[j for i,j in flat_list2]
df5['target']=[i for i,j in flat_list2]

df_fi=pd.concat([df4,df5])

len(df_fi)
df_fi.drop_duplicates(keep='last',inplace=True)

len(df_fi)
# total of 70134 bi-directional edges

df_fi.to_csv('graph.csv',sep=",",index=False)

# Use graph.csv in arglite to visualize the graph 
