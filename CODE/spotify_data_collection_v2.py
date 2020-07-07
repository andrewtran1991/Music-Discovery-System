import requests
import pandas as pd
import csv
import time
import json
import sys
import imp
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2


imp.reload(sys)

CLIENT_ID='026d8b9473184069b6111d398351f121'
CLIENT_SECRET='c91f27b5c9a64f0ba5af83d7d2a8d347'

credentials = oauth2.SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET)

access_token = credentials.get_access_token()

print('start..'+access_token)
#set debug prints
debug = True

def main():
    
    queries = ['1950']
    #queries = ['1995','1996','1997','1998','1999','2000','2001',
    #            '2002','2003','2004','2005','2006','2007','2008',
    #            '2009','2010','2011','2012','2013','2014','2015',
    #            '2016','2017','2018','2019','2020']
    
    num_tracks_per_query = 2000
    
    for query in queries:        
        ltrack = []
        song_ids = []
        artist_ids = []
        album_ids = []
        
        audioF = []
        artist_data = []
        album_data = []

        
        col1 = [   'song_id', 'song_name', 
                   'artist_id',   'artist_name', 'album_id',                   
                   'explicit',    'disc_number',   'track_number']
        
        
        col2 =  [  'song_id', 'uri',
                   'tempo', 'type',
                   'key', 'loudness',
                   'mode', 'speechiness',
                   'liveness', 'valence',
                   'danceability', 'energy',
                   'track_href', 'analysis_url',
                   'duration_ms', 'time_signature',
                   'acousticness', 'instrumentalness' ]
        
        col3 =  [  'artist_id',  'artist_genres',  'artist_popularity']
        
        col4 =  [  'album_id',   'album_name',  'album_genres',   'album_popularity',  'album_release_date']
        
        n = 0 
        idx = 0
        
        while idx < num_tracks_per_query:              
            num_tracks_per_query = API_search_request_albums(query, 'album', 50, idx, ltrack, song_ids, artist_ids, album_ids, num_tracks_per_query)   
            n +=1
            print(('\n>> this is iteration: '+ str(n) + ' - album count: ' + str(len(album_ids))))
            idx += 50 
            # Limit API requests to at most 3ish calls / second
            time.sleep(0.3)
            #time.sleep(0.5)
        
        print('year: ' + query + ' - get tracks')
        for alb_id in album_ids:
            API_get_tracks_from_album(alb_id, ltrack, song_ids, artist_ids)
            time.sleep(0.3)
            #time.sleep(0.5)
            
        print('year: ' + query + ' - total tracks:' + str(len(song_ids)))
        ## spotify API "search" option vs here track/audiofeature query        
        print('year: ' + query + ' - API_get_audio_feature')
        for idx in range(0, len(song_ids), 50):
            API_get_audio_feature(song_ids[idx: idx+50], audioF)
            time.sleep(0.3)
            #time.sleep(0.5)
            
        print('year: ' + query + ' - API_get_artists')
        for idx in range(0, len(artist_ids), 50):
            API_get_artists(artist_ids[idx: idx+50], artist_data)
            time.sleep(0.3)
            #time.sleep(0.5)
        
        print('year: ' + query + ' - API_get_albums')
        for idx in range(0, len(album_ids), 20):
            API_get_albums(album_ids[idx: idx+20], album_data)
            time.sleep(0.3)
            #time.sleep(0.5)    
        
        
        print('year: ' + query + ' - join and merge')
        df1 = pd.DataFrame(ltrack, columns=col1)
        
        df2 = pd.DataFrame(audioF, columns=col2)
                
        df3 = pd.DataFrame(artist_data, columns=col3)
        
        df4 = pd.DataFrame(album_data, columns=col4)
        
        df = pd.merge(pd.merge(pd.merge(df1,df4, on='album_id', how='inner'),df3,on='artist_id', how='inner'),df2, on='song_id', how='inner')
        
        filename = "data/"+query + '.csv'                      
        
        df.to_csv(filename, sep='\t')
        
        print ('finish - year: ' + query + ' - total: ' + str(len(song_ids)))
        print (query)

def API_search_request(keywords, search_type, results_limit, results_offset, ltrack, song_ids, artist_ids, album_ids):

    off = str(results_offset)
    lim = str(results_limit)

    url = 'https://api.spotify.com/v1/search?q=year:'+ keywords +'&type=' + search_type +'&offset='+ off +'&limit=' + lim
    headers={"Accept": "application/json" , "Authorization": "Bearer "+access_token}
    r = requests.get(url, headers=headers)
    print( r)

    if r: 
       j = r.json()
    else:
      return r


    litem = j['tracks']['items']
    #print("total: " + str(j['tracks']['total']))
    
    try:
        for l in litem:
        
            if l['id'] not in song_ids:
                song_ids.append( l['id'] )

            if l['artists'][0]['id'] not in artist_ids:
                artist_ids.append( l['artists'][0]['id'] )

            if l['album']['id'] not in album_ids:
                album_ids.append(  l['album']['id'] )
        
        
            k =   [  l['popularity'],
        
                     l['id'], 
                     l['artists'][0]['id'],
                     l['album']['id'],

                     l['name'],
                     l['artists'][0]['name'],
                     l['album']['name'],

                     l['explicit'], 
                     l['disc_number'],
                     l['track_number']]
        
            ltrack.append(k)
    except:
         ValueError
      
   # f.close()
    #return j
def API_get_tracks_from_album(alb_id, ltrack, song_ids, artist_ids):


    url = 'https://api.spotify.com/v1/albums/'+alb_id+'/tracks?limit=50'
    headers={"Accept": "application/json" , "Authorization": "Bearer "+access_token}
    r = requests.get(url, headers=headers)
    #print( r)

    if r: 
       j = r.json()
    else:
      return r


    litem = j['items']
    #print(len(ll))
    #print("total: " + str(j['tracks']['total']))
    #print("next: " + j['tracks']['next'])
    
    try:
        for l in litem:
        
            if l['id'] not in song_ids:
                song_ids.append( l['id'] )
            
            if l['artists'][0]['id'] not in artist_ids:
                artist_ids.append( l['artists'][0]['id'] )        
            
            k =   [  l['id'],
                     l['name'],
                     l['artists'][0]['id'],
                     l['artists'][0]['name'],
                     alb_id,
                     l['explicit'], 
                     l['disc_number'],
                     l['track_number']]
            
            ltrack.append(k)
            print('     ' + l['name'] + ' by ['+ l['artists'][0]['name'] +']')
    except:
         ValueError
      
   # f.close()
    #return j

def API_search_request_albums(keywords, search_type, results_limit, results_offset, ltrack, song_ids, artist_ids, album_ids, num_tracks_per_query):

    off = str(results_offset)
    lim = str(results_limit)

    url = 'https://api.spotify.com/v1/search?q=year:'+ keywords +'&type=album&offset='+ off +'&limit=' + lim
    headers={"Accept": "application/json" , "Authorization": "Bearer "+access_token}
    r = requests.get(url, headers=headers)
    #print( r)
    

    if r: 
       j = r.json()
    else:
      #return r
      return 0


    litem = j['albums']['items']
    
    num_tracks_per_query = j['albums']['total']
    #print(len(ll))
    #print("total: " + str(j['tracks']['total']))
    print("num_tracks_per_query: " + str(num_tracks_per_query))
    
    try:
        for l in litem:

            if l['id'] not in album_ids:
                album_ids.append(  l['id'] )        
            
    except:
         ValueError
    return num_tracks_per_query
   # f.close()
    #return j


def API_get_audio_feature(songids, audioF):
    
    #print(songids)
    #print '>> call art several'
    track_ids = ','.join(songids)

    url = 'https://api.spotify.com/v1/audio-features?ids=' + track_ids
   
    headers={"Accept": "application/json" , "Authorization": "Bearer "+access_token}
    r = requests.get(url,headers=headers)
    # print(r)
    if r: 
      j = r.json()
    else:
      return r
    
    # print(j)
    ll = j['audio_features']

    try:

        for l in ll:
            k =  [  l['id'],l['uri'],
                    l['tempo'],l['type'],
                    l['key'],l['loudness'],
                    l['mode'],l['speechiness'],
                    l['liveness'],l['valence'],
                    l['danceability'],l['energy'],
                    l['track_href'],l['analysis_url'],
                    l['duration_ms'],l['time_signature'],
                    l['acousticness'],l['instrumentalness'] ]

            audioF.append(k)
        
    except:
        ValueError
    
        

    #return j

def API_get_artists(artist_ids, artist_data):

    art_ids = ','.join(artist_ids)

    url = 'https://api.spotify.com/v1/artists?ids=' + art_ids
    headers={"Accept": "application/json" , "Authorization": "Bearer "+access_token}
    r = requests.get(url, headers=headers)

    if r:
       j = r.json()
    else:
       #print 'for this specific art_ids, response reaches maximum, return'
       return r

    
    ll = j['artists']

    try:
        for l in ll:
        
            k = [  l['id'], 
                   l['genres'],
                   l['popularity'] ]

            artist_data.append(k)
    
    except:
        ValueError
    


def API_get_albums(album_ids, album_data):
   

    alb_ids = ','.join(album_ids)

    url = 'https://api.spotify.com/v1/albums?ids=' + alb_ids
    headers={"Accept": "application/json" , "Authorization": "Bearer "+access_token}
    r = requests.get(url, headers=headers)
    # print(r)
    if r:
       j = r.json()
    #    print(j)
    else:
       return r

    
    ll = j['albums']
    
    try:
        for l in ll:
            # print(l)
            k = [  l['id'], 
                   l['name'],
                   l['genres'],
                   l['popularity'],
                   l['release_date'] ]

            album_data.append(k)
    
    except:
        ValueError


if __name__ == '__main__':
    main()
