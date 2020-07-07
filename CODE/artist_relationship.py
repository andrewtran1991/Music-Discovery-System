# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:25:22 2020

@author: npung3
"""


import pandas as pd
import sqlite3
conn = sqlite3.connect('data\spotify.db')

#data taken from 
#https://musicbrainz.org/doc/MusicBrainz_Database/Download
#download the core dump mbdump.tar.bz2
column_list = ["id","gid","name","sort_name","begin_date_year","begin_date_month","begin_date_day","end_date_year","end_date_month","end_date_day","artist_type","area","gender","comment","something","last_updated","updates_pending","begin_area","end_area"]
artist_data = pd.read_csv("data\\artist","\t",names=column_list,encoding='utf8')

df = pd.read_sql_query("SELECT DISTINCT artist_id, artist_name FROM spotify", conn)
df["lower_artist_name"] = df["artist_name"].str.lower()
artist_data["lower_artist_name"] = artist_data["name"].str.lower()
merged_artist_data = pd.merge(df, artist_data, how='inner', on='lower_artist_name')
merged_artist_data = merged_artist_data[['artist_id','artist_name','lower_artist_name','id','gid','name']]
merged_artist_data["artist_id_1"] = merged_artist_data["id"]
merged_artist_data["artist_id_2"] = merged_artist_data["id"]
merged_artist_data["sp_artist_id_1"] = merged_artist_data["artist_id"]
merged_artist_data["sp_artist_id_2"] = merged_artist_data["artist_id"]
merged_artist_data["sp_artist_name_1"] = merged_artist_data["artist_name"]
merged_artist_data["sp_artist_name_2"] = merged_artist_data["artist_name"]


column_list = ['id', "link_id","artist_id", "event_id","edits_pending","c1","c2","c3",'c4']
event_data = pd.read_csv("data\\l_artist_event", "\t",names=column_list,encoding='utf8')

event_data["artist_id_1"] = event_data["artist_id"]
event_data["artist_id_2"] = event_data["artist_id"]

event_data_all = pd.merge(event_data[['artist_id_1','event_id']], event_data[["artist_id_2" ,'event_id']], how='inner',on='event_id')

event_data_all = event_data_all[['artist_id_1','event_id',"artist_id_2"]]

event_data_all = event_data_all.loc[event_data_all['artist_id_1'] != event_data_all['artist_id_2']]

merged_artist_event_data1 = pd.merge(event_data_all, merged_artist_data[["artist_id_1","sp_artist_id_1","sp_artist_name_1"]], how='inner',on='artist_id_1')

merged_artist_event_data = pd.merge(merged_artist_event_data1, merged_artist_data[["artist_id_2","sp_artist_id_2","sp_artist_name_2"]], how='inner',on='artist_id_2')


column_list = ["event_id","gid","event_name","c1","c2","c3","c4","c6","c7","c8","c9","c10","c11","c12","c13",'c14','c15']
event_info = pd.read_csv("data\\event","\t",names=column_list,encoding='utf8')

all_event_artists = pd.merge(merged_artist_event_data,event_info[['event_id','event_name']], how='inner', on='event_id')

spotify_relationships = all_event_artists[["sp_artist_id_1","sp_artist_name_1", "sp_artist_id_2","sp_artist_name_2"]]

spotify_relationships = spotify_relationships.sort_values(["sp_artist_id_1","sp_artist_name_1", "sp_artist_id_2","sp_artist_name_2"], inplace = False) 
  
# dropping ALL duplicte values 
spotify_relationships = spotify_relationships.drop_duplicates(subset =["sp_artist_id_1","sp_artist_name_1", "sp_artist_id_2","sp_artist_name_2"], 
                     keep = False, inplace = False) 
spotify_relationships.to_csv("data\spotify_relationships.tsv", sep='\t', header=True, index=False)
