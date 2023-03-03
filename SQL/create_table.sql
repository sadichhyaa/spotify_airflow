--creating tracks table

CREATE TABLE IF NOT EXISTs spotify_schema.spotify_tracks(
    unique_identifier TEXT PRIMARY KEY NOT NULL,
    song_id TEXT NOT NULL,
    song_name TEXT,
    song_duration INTEGER,
    song_url TEXT,
    popularity SMALLINT,
    date_time_played TIMESTAMP,
    album_id TEXT,
    artist_id TEXT,
    date_time_inserted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Creating the Album Table
CREATE TABLE IF NOT EXISTS spotify_schema.spotify_album(
    album_id TEXT NOT NULL PRIMARY KEY,
    name TEXT,
    release_date TEXT,
    total_tracks SMALLINT,
    url TEXT
    );

-- Creating the Artist Table 
CREATE TABLE IF NOT EXISTS spotify_schema.spotify_artists(
    artist_id TEXT PRIMARY KEY NOT NULL,
    name TEXT,
    url TEXT);
