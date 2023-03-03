import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from dotenv import load_dotenv
import sys
import os
import json

load_dotenv()


def extract_func():
    spotify_redirect_url = "http://localhost"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('spotify_client_id'),
                                                   client_secret=os.getenv('spotify_client_secret'),
                                                   redirect_uri=spotify_redirect_url,
                                                   scope="user-read-recently-played"))
    recently_played= sp.current_user_recently_played(limit=50)
    if len(recently_played) ==0:
        sys.exit("No results recieved from Spotify")
    
    album_id=[]
    album_name=[]
    album_release_date=[]
    album_total_tracks=[]
    album_url=[]
    for row in recently_played['items']:
        album_id.append(row['track']['album']['id'])
        album_name.append(row['track']['album']['name'])
        album_release_date.append( row['track']['album']['release_date'])
        album_total_tracks.append(row['track']['album']['total_tracks'])
        album_url.append(row['track']['album']['external_urls']['spotify'])
        
    album_element = {'album_id':album_id,'name':album_name,'release_date':album_release_date,
                            'total_tracks':album_total_tracks,'url':album_url}
        # print(album_element)
    # print(album_list)
    
    

    artist_id=[]
    artist_name=[]
    artist_url=[]
    for row in recently_played['items']:
        artist_id.append(row['track']['artists'][0]['id'])
        artist_name.append(row['track']['artists'][0]['name'])
        artist_url.append(row['track']['artists'][0]['external_urls']['spotify'])

    artist_element = {'artist_id':artist_id,'artist_name':artist_name,'artist_url':artist_url}

    song_id=[]
    song_name=[]
    song_duration=[]
    song_url=[]
    song_popularity=[]
    song_played_at=[]

    for row in recently_played['items']:
        song_id.append(row['track']['id'])
        song_name.append(row['track']['name'])
        song_duration.append(row['track']['duration_ms'])
        song_url.append(row['track']['external_urls']['spotify'])
        song_popularity.append(row['track']['popularity'])
        song_played_at.append(row['played_at'])
    song_element={'song_id':song_id,'song_name':song_name,'song_duration':song_duration,'song_url':song_url,'song_popularity':song_popularity,'song_played_at':song_played_at,'album_id':album_id,'artist_id':artist_id}

    return album_element,artist_element,song_element


