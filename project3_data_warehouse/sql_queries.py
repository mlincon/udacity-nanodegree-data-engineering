import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays CASCADE"
user_table_drop = "DROP TABLE IF EXISTS users CASCADE"
song_table_drop = "DROP TABLE IF EXISTS songs CASCADE"
artist_table_drop = "DROP TABLE IF EXISTS artists CASCADE"
time_table_drop = "DROP TABLE IF EXISTS time CASCADE"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE staging_events (
        artist          VARCHAR(MAX)
        , auth          VARCHAR(256)
        , firstName     VARCHAR(MAX)
        , gender        CHAR(1)
        , itemInSession INTEGER
        , lastName      VARCHAR(MAX)
        , length        DOUBLE PRECISION
        , level         VARCHAR(256)
        , location      VARCHAR(MAX)
        , method        CHAR(10)
        , page          VARCHAR(256)
        , registration  DOUBLE PRECISION
        , sessionId     INTEGER
        , song          VARCHAR(MAX)
        , status        INTEGER
        , ts            BIGINT
        , userAgent     VARCHAR(MAX) 
        , userId        VARCHAR(300)
    )
""")

staging_songs_table_create = ("""
    CREATE TABLE staging_songs (
        num_songs           INTEGER
        , artist_id         VARCHAR(300)
        , artist_latitude   DOUBLE PRECISION
        , artist_longitude  DOUBLE PRECISION 
        , artist_location   VARCHAR(MAX)
        , artist_name       VARCHAR(MAX)
        , song_id           VARCHAR(300)
        , title             VARCHAR(MAX)
        , duration          DOUBLE PRECISION
        , year              SMALLINT
    )
""")

songplay_table_create = ("""
    CREATE TABLE songplays (
        songplay_id     INTEGER IDENTITY(0,1) PRIMARY KEY
        , start_time    TIMESTAMP REFERENCES time (start_time)
        , user_id       VARCHAR(300) REFERENCES users (user_id)
        , level         VARCHAR(MAX)
        , song_id       VARCHAR(300) REFERENCES songs (song_id)
        , artist_id     VARCHAR(MAX) REFERENCES artists (artist_id)
        , session_id    INTEGER
        , location      VARCHAR(MAX)
        , user_agent    VARCHAR(MAX)
    )
""")

user_table_create = ("""
    CREATE TABLE users (
        user_id         VARCHAR(300) PRIMARY KEY
        , first_name    VARCHAR(MAX)
        , last_name     VARCHAR(MAX)
        , gender        CHAR(1)
        , level         VARCHAR(256)
    )
""")

song_table_create = ("""
    CREATE TABLE songs (
        song_id     VARCHAR(300) PRIMARY KEY
        , title     VARCHAR(MAX)
        , artist_id VARCHAR(300)
        , year      SMALLINT
        , duration  DOUBLE PRECISION
    )
""")

artist_table_create = ("""
    CREATE TABLE artists (
        artist_id   VARCHAR(300) PRIMARY KEY
        , name      VARCHAR(MAX)
        , location  VARCHAR(MAX)
        , lattitude DOUBLE PRECISION
        , longitude DOUBLE PRECISION
    )
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time  TIMESTAMP PRIMARY KEY
        , hour      SMALLINT
        , day       SMALLINT
        , week      SMALLINT
        , month     SMALLINT
        , year      SMALLINT
        , weekday   CHAR(30)
    )
""")

# STAGING TABLES
# ref: https://docs.aws.amazon.com/redshift/latest/dg/r_COPY_command_examples.html#r_COPY_command_examples-copy-from-json
staging_events_copy = ("""
    copy staging_events
    from {} 
    iam_role '{}'
    region 'us-west-2'
    json {};
""").format(config.get("S3", "LOG_DATA"),
            config.get("IAM_ROLE", "ARN"),
            config.get("S3", "LOG_JSONPATH"))

staging_songs_copy = ("""
    copy staging_songs 
    from {} 
    iam_role '{}'
    region 'us-west-2'
    json 'auto';
""").format(config.get("S3", "SONG_DATA"),
            config.get("IAM_ROLE", "ARN"))

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (
        start_time
        , user_id
        , level
        , song_id
        , artist_id
        , session_id
        , location
        , user_agent
    )
    SELECT
        -- ref: https://www.fernandomc.com/posts/redshift-epochs-and-timestamps/
        timestamp 'epoch' +  (events.ts/1000)* interval '1 second' AS start_time
        , events.userId     AS user_id
        , events.level      AS level
        , songs.song_id     AS song_id
        , songs.artist_id   AS artist_id
        , events.sessionId  AS session_id
        , events.location   AS location
        , events.userAgent  AS user_agent
    JOIN staging_songs songs
    FROM staging_events events
        ON songs.artist_name = events.artist
        AND songs.title = events.song
    WHERE events.page = 'NextSong'
""")

user_table_insert = ("""
    INSERT INTO users (
        user_id
        , first_name
        , last_name
        , gender
        , level
    )
    SELECT DISTINCT
        events.userId       AS user_id
        , events.firstName  AS first_name
        , events.lastName   AS last_name
        , events.gender     AS gender
        , events.level      AS level
    FROM staging_events events
""")

song_table_insert = ("""
    INSERT INTO songs (
        song_id
        , title
        , artist_id
        , year
        , duration
    )
    SELECT DISTINCT
        songs.song_id       AS song_id
        , songs.title       AS title
        , songs.artist_id   AS artist_id
        , songs.year        AS year
        , songs. duration   AS duration
    FROM staging_songs songs

""")

artist_table_insert = ("""
    INSERT INTO artists (
        artist_id
        , name
        , location
        , latitude
        , longitude
    )
    SELECT DISTINCT
        songs.artist_id             AS artist_id
        , songs.artist_name         AS name
        , songs.artist_location     AS location
        , songs.artist_latitude     AS lattitude
        , songs.artist_longitude    AS longitude
    FROM staging_songs songs
""")

# ref: https://docs.aws.amazon.com/redshift/latest/dg/r_Dateparts_for_datetime_functions.html
time_table_insert = ("""
    INSERT INTO times (
        start_time
        , hour
        , day
        , week
        , month
        , year
        , weekday
    )
    SELECT
        t.start_time                        AS start_time
        , DATE_PART(HOUR, start_time)       AS hour
        , DATE_PART(DAY, start_time)        AS day
        , DATE_PART(WEEK, start_time)       AS week
        , DATE_PART(MONTH, start_time)      AS month
        , DATE_PART(YEAR, start_time)       AS year
        , DATE_PART(WEEKDAY, start_time)    AS weekday
    FROM (
        SELECT DISTINCT
            timestamp 'epoch' +  (events.ts/1000)* interval '1 second' AS start_time
        FROM staging_events events
    ) t

""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop, songplay_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert, song_table_insert, artist_table_insert, time_table_insert, songplay_table_insert]
