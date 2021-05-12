# DROP TABLES

music_app_history_table_drop = "DROP TABLE IF EXISTS music_app_history"
music_app_users_table_drop = "DROP TABLE IF EXISTS music_app_users"
music_app_songs_table_drop = "DROP TABLE IF EXISTS music_app_songs"


# CREATE TABLES

## Query 1:  Give me the artist, song title and song's length in the music app history that was heard during
## sessionId = 338, and itemInSession = 4
music_app_history_table_create = ("""
CREATE TABLE IF NOT EXISTS music_app_history (
                            artist varchar, 
                            song varchar, 
                            length float, 
                            session_id int, 
                            itemInSession int, 
                            PRIMARY KEY ((session_id), itemInSession))
""")

## Query 2: Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name)
## for userid = 10, sessionid = 182
music_app_users_table_create = ("""
CREATE TABLE IF NOT EXISTS music_app_users (
                            artist varchar, 
                            song varchar, 
                            firstname varchar, 
                            lastname varchar, 
                            session_id int, 
                            itemInSession int, 
                            user_id int, 
                            PRIMARY KEY ((user_id), session_id, itemInSession))
""")

## Query 3: Give me every user name (first and last) in my music app history who listened to the song 
## 'All Hands Against His Own'
music_app_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS music_app_songs (
                            firstname varchar, 
                            lastname varchar, 
                            session_id int, 
                            itemInSession int, 
                            user_id int, 
                            song varchar, 
                            PRIMARY KEY ((song), session_id, itemInSession))
""")





# INSERT RECORDS


music_app_history_table_insert = ("""
INSERT INTO music_app_history( 
                artist, 
                song, 
                length, 
                session_id, 
                itemInSession)
                VALUES (%s, %s, %s, %s, %s)
""")



music_app_users_table_insert = ("""
INSERT INTO music_app_users( 
                artist, 
                song,
                firstname,
                lastname,
                session_id,
                itemInSession,
                user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
""")


music_app_songs_table_insert = ("""
INSERT INTO music_app_songs( 
                firstname,
                lastname,
                session_id,
                itemInSession,
                user_id, 
                song)
                VALUES (%s, %s, %s, %s, %s, %s)
""")



# SELECT

query1_select = ("""
SELECT artist, song, length
    FROM music_app_history 
    WHERE session_id = %s 
    AND itemInSession = %s             
""")

query2_select = ("""
SELECT artist, song, firstname, lastname
    FROM music_app_users 
    WHERE user_id = %s 
    AND session_id = %s             
""")


query3_select = ("""
SELECT firstname, lastname
    FROM music_app_songs 
    WHERE song = %s 
""")


# QUERY LISTS

create_table_queries = [music_app_history_table_create, music_app_users_table_create, music_app_songs_table_create]
drop_table_queries = [music_app_history_table_drop, music_app_users_table_drop, music_app_songs_table_drop]