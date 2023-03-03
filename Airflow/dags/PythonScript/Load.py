import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os 
import pandas as pd
from Transform import transform_func

def load_func():
    load_dotenv()
    song_df,album_df,artist_df=transform_func()


    hostname=os.getenv('hostname')
    database=os.getenv('database')
    user_name=os.getenv('user_name')
    pwd=os.getenv('pwd')
    port_id=os.getenv('port_id')
    # print(os.getenv('user_name'),)
    # print(os.getenv('pwd'))
    # print(os.getenv('database'))
    # print(os.getenv('hostname'))
    # print(os.getenv('port_id'))

    #loading data into temporary table
    connection  = psycopg2.connect(user=user_name,
            password=pwd,
                database=database,
                host=hostname,
                port=port_id)

    cur=connection.cursor()
    engine = create_engine(f'postgresql+psycopg2://{user_name}:{pwd}@{hostname}/{database}')
    conn_eng=engine.raw_connection()
    cur_eng=conn_eng.cursor()


    #Creating temporary table for tracks:(to extract unique data evrytime)

    cur_eng.execute(

        """
        CREATE TEMP TABLE IF NOT EXISTS temp_track AS SELECT * FROM spotify_schema.spotify_tracks LIMIT 0
        """
    )

    song_df.to_sql("temp_track", con=engine, if_exists='append',index=False)
    conn_eng.commit()

    cur.execute(
        """
        INSERT INTO spotify_schema.spotify_tracks
        SELECT temp_track.*
        FROM   temp_track
        LEFT   JOIN spotify_schema.spotify_tracks USING (unique_id)
        WHERE  spotify_schema.spotify_tracks.unique_id IS NULL;

        DROP TABLE temp_track
        """
    )

    connection.commit()

    #Album temp table:

    cur_eng.execute(

        """
        CREATE TEMP TABLE IF NOT EXISTS temp_album AS SELECT * FROM spotify_schema.spotify_album LIMIT 0
        """
    )

    album_df.to_sql("temp_album", con=engine,if_exists='append', index=False)
    conn_eng.commit()

    #moving data from temp table to schema table
    cur.execute(
        """
        INSERT INTO spotify_schema.spotify_album
        SELECT temp_album.*
        FROM   temp_album
        LEFT   JOIN spotify_schema.spotify_album USING (album_id)
        WHERE  spotify_schema.spotify_album.album_id IS NULL;
        """
    )

    connection.commit()

    # #Artist temop table
    cur_eng.execute(
        """
        CREATE TEMP TABLE IF NOT EXISTS temp_artist AS SELECT * FROM spotify_schema.spotify_artists LIMIT 0
        """)
    artist_df.to_sql("temp_artist", con = engine, if_exists='append', index = False)
    conn_eng.commit()

    cur.execute(
        """
        INSERT INTO spotify_schema.spotify_artists
        SELECT temp_artist.*
        FROM   temp_artist
        LEFT   JOIN spotify_schema.spotify_artists USING (artist_id)
        WHERE  spotify_schema.spotify_artists.artist_id IS NULL;
        
        DROP TABLE temp_artist""")
    connection.commit()
    
    

load_func()