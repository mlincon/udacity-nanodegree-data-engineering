# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

## records in log data associated with song plays
songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id SERIAL PRIMARY KEY, 
        start_time TIMESTAMP REFERENCES time (start_time), 
        user_id INT REFERENCES users (user_id), 
        level TEXT, 
        song_id VARCHAR(180) REFERENCES songs (song_id), 
        artist_id VARCHAR(180) REFERENCES artists (artist_id), 
        session_id INT, 
        location TEXT, 
        user_agent TEXT
    )
""")

## users in the app
user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY, 
        first_name TEXT, 
        last_name TEXT, 
        gender CHAR(1),
        level TEXT
    )
""")

## songs in music database
song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id VARCHAR(180) PRIMARY KEY, 
        title TEXT, 
        artist_id VARCHAR(180), 
        year INT, 
        duration FLOAT
    )
""")

## artists in music database
artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id VARCHAR(180) PRIMARY KEY, 
        name TEXT, 
        location TEXT, 
        latitude FLOAT, 
        longitude FLOAT
    )
""")

## timestamps of records in songplays broken down into specific units
time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time TIMESTAMP PRIMARY KEY, 
        hour INT, 
        day INT, 
        week INT, 
        month INT, 
        year INT, 
        weekday VARCHAR
    )
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO 
        songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
""")

user_table_insert = ("""
    INSERT INTO 
        users (user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id)
        DO UPDATE SET 
            level = EXCLUDED.level
    ;
""")

song_table_insert = ("""
    INSERT INTO 
        songs (song_id, title, artist_id, year, duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (song_id)
        DO NOTHING
    ;
""")

artist_table_insert = ("""
    INSERT INTO 
        artists (artist_id, name, location, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id)
        DO UPDATE SET
            location = EXCLUDED.location,
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude
    ;
""")


time_table_insert = ("""
    INSERT INTO 
        time (start_time, hour, day, week, month, year, weekday)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT
        DO NOTHING
    ;
""")

# FIND SONGS

song_select = ("""
    SELECT 
        song_id
        , artists.artist_id
    FROM songs 
    JOIN artists 
        ON songs.artist_id = artists.artist_id
    WHERE 
        songs.title = %s
        AND artists.name = %s
        AND songs.duration = %s
    ;
""")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [user_table_drop, song_table_drop, artist_table_drop, time_table_drop, songplay_table_drop]