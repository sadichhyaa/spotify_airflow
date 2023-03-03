import pandas as pd
from .Extract import extract_func



def transform_func():
    album_dict, artist_dict, song_dict = extract_func()

    # converting dict to dataframe.
    album_df = pd.DataFrame.from_dict(album_dict)
    

    artist_df = pd.DataFrame.from_dict(artist_dict)
    

    song_df = pd.DataFrame.from_dict(song_dict)
    

    # cleaning album data.
    album_df = album_df.drop_duplicates(subset=['album_id'])
    album_df['release_date'] = pd.to_datetime(album_df['release_date'])
    album_df.to_csv('album.csv', index=False)

    # cleaning artist data
    artist_df = artist_df.drop_duplicates(subset=['artist_id'])
    artist_df.to_csv('artist.csv', index=False)

    # cleaning song data

    song_df['song_played_at'] = pd.to_datetime(song_df['song_played_at'])
    # converting to kathmandu timezone
    song_df['song_played_at'].dt.tz_convert('Asia/Kathmandu')
    # removing timezone after + // datetime -> string
    song_df['song_played_at'] = song_df['song_played_at'].astype(str).str[:-7]
    # string -> datetime
    song_df['song_played_at'] = pd.to_datetime(song_df['song_played_at'])
    # getting unix timestamp to create unique identifier
    song_df['UNIX_Time_Stamp'] = (
        song_df['song_played_at'] - pd.Timestamp("1970-01-01"))//pd.Timedelta('1s')
    # creating unique identifier
    song_df['unique_id'] = song_df['song_id'] + \
        '-'+song_df['UNIX_Time_Stamp'].astype(str)
    # creating df without unix column
    song_df = song_df[['unique_id', 'song_id', 'song_name', 'song_duration',
                       'song_url', 'song_popularity', 'song_played_at', 'album_id', 'artist_id']]
    song_df.to_csv('song.csv', index=False)
    
    return song_df,album_df,artist_df
                       


