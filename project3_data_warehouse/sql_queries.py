import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS user"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events (
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
    CREATE TABLE IF NOT EXISTS staging_songs (
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
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id     IDENTITY(0,1) PRIMARY KEY
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
    CREATE TABLE IF NOT EXISTS users (
        user_id         VARCHAR(300) PRIMARY KEY
        , first_name    VARCHAR(MAX)
        , last_name     VARCHAR(MAX)
        , gender        CHAR(1)
        , level         VARCHAR(256)
    )
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id     VARCHAR(300) PRIMARY KEY
        , title     VARCHAR(MAX)
        , artist_id VARCHAR(300)
        , year      SMALLINT
        , duration  DOUBLE PRECISION
    )
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id   VARCHAR(300) PRIMARY KEY
        , name      VARCHAR(MAX)
        , location  VARCHAR(MAX)
        , lattitude DOUBLE PRECISION
        , longitude DOUBLE PRECISION
    )
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS times (
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
    iam_role {}
    region 'us-west-2'
    json '{}';
""").format(
    config.get["S3"]["LOG_DATA"],
    config.get["IAM_ROLE"]["ARN"],
    config.get["S3"]["LOG_JSONPATH"]
)

staging_songs_copy = ("""
    copy staging_songs 
    from {} 
    iam_role {}
    region 'us-west-2'
    json 'auto';
""").format(
    config.get["S3"]["SONG_DATA"],
    config.get["IAM_ROLE"]["ARN"]
)

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
