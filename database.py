#!/usr/bin/env python3
"""
MediaServer Database module.
Contains all interactions between the webapp and the queries to the database.
"""

import configparser
import json
import sys
from modules import pg8000


################################################################################
#   Welcome to the database file, where all the query magic happens.
#   My biggest tip is look at the *week 8 lab*.
#   Important information:
#       - If you're getting issues and getting locked out of your database.
#           You may have reached the maximum number of connections.
#           Why? (You're not closing things!) Be careful!
#       - Check things *carefully*.
#       - There may be better ways to do things, this is just for example
#           purposes
#       - ORDERING MATTERS
#           - Unfortunately to make it easier for everyone, we have to ask that
#               your columns are in order. WATCH YOUR SELECTS!! :)
#   Good luck!
#       And remember to have some fun :D
################################################################################

#############################
#                           #
# Database Helper Functions #
#                           #
#############################


#####################################################
#   Database Connect
#   (No need to touch
#       (unless the exception is potatoing))
#####################################################

def database_connect():
    """
    Connects to the database using the connection string.
    If 'None' was returned it means there was an issue connecting to
    the database. It would be wise to handle this ;)
    """
    # Read the config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'database' not in config['DATABASE']:
        config['DATABASE']['database'] = config['DATABASE']['user']

    # Create a connection to the database
    connection = None
    try:
        # Parses the config file and connects using the connect string
        connection = pg8000.connect(database=config['DATABASE']['database'],
                                    user=config['DATABASE']['user'],
                                    password=config['DATABASE']['password'],
                                    host=config['DATABASE']['host'])
    except pg8000.OperationalError as operation_error:
        print("""Error, you haven't updated your config.ini or you have a bad
        connection, please try again. (Update your files first, then check
        internet connection)
        """)
        print(operation_error)
        return None

    # return the connection to use
    return connection


##################################################
# Print a SQL string to see how it would insert  #
##################################################

def print_sql_string(inputstring, params=None):
    """
    Prints out a string as a SQL string parameterized assuming all strings
    """

    if params is not None:
        if params != []:
           inputstring = inputstring.replace("%s","'%s'")

    print(inputstring % params)

#####################################################
#   SQL Dictionary Fetch
#   useful for pulling particular items as a dict
#   (No need to touch
#       (unless the exception is potatoing))
#   Expected return:
#       singlerow:  [{col1name:col1value,col2name:col2value, etc.}]
#       multiplerow: [{col1name:col1value,col2name:col2value, etc.},
#           {col1name:col1value,col2name:col2value, etc.},
#           etc.]
#####################################################

def dictfetchall(cursor,sqltext,params=None):
    """ Returns query results as list of dictionaries."""

    result = []
    if (params is None):
        print(sqltext)
    else:
        print("we HAVE PARAMS!")
        print_sql_string(sqltext,params)

    cursor.execute(sqltext,params)
    cols = [a[0].decode("utf-8") for a in cursor.description]
    print(cols)
    returnres = cursor.fetchall()
    for row in returnres:
        result.append({a:b for a,b in zip(cols, row)})
    # cursor.close()
    return result


def dictfetchone(cursor, sqltext, params=None):
    """ Returns query results as list of dictionaries."""
    # cursor = conn.cursor()
    result = []
    cursor.execute(sqltext, params)
    cols = [a[0].decode("utf-8") for a in cursor.description]
    returnres = cursor.fetchone()
    result.append({a: b for a, b in zip(cols, returnres)})
    return result


#####################################################
#   Query (1)
#   Login
#####################################################

def check_login(username, password):
    """
    Check that the users information exists in the database.
        - True => return the user data
        - False => return None
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below in a manner similar to Wk 08 Lab to log the user in #
        #############################################################################

        sql = """
        SELECT      *
        FROM        mediaserver.UserAccount
        WHERE       username = %s AND password = %s
        """

        print(username)
        print(password)

        r = dictfetchone(cur, sql, (username, password))
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Is Superuser? -
#   is this required? we can get this from the login information
#####################################################

def is_superuser(username):
    """
    Check if the user is a superuser.
        - True => Get the departments as a list.
        - False => Return None
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        SELECT      isSuper
        FROM        mediaserver.UserAccount
        WHERE       username=%s AND isSuper
        """
        print("username is: " + username)
        cur.execute(sql, (username))
        r = cur.fetchone()  # Fetch the first row
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (1 b)
#   Get user playlists
#####################################################
def user_playlists(username):
    """
    Check if user has any playlists
        - True -> Return all user playlists
        - False -> Return None
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        ###############################################################################
        # Fill in the SQL below and make sure you get all the playlists for this user #
        ###############################################################################
        sql = """
        SELECT      collection_id, collection_name, count(collection_id)
        FROM        mediaserver.MediaCollection NATURAL JOIN mediaserver.MediaCollectionContents
        WHERE       username = %s
        GROUP BY    collection_id
        ORDER BY    collection_id
        """

        print("username is: " + username)
        r = dictfetchall(cur, sql, (username,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting User Playlists:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (1 a)
#   Get user podcasts
#####################################################
def user_podcast_subscriptions(username):
    """
    Get user podcast subscriptions.
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #################################################################################
        # Fill in the SQL below and get all the podcasts that the user is subscribed to #
        #################################################################################

        sql = """
        SELECT      podcast_id, podcast_title, podcast_uri, podcast_last_updated
        FROM        mediaserver.Podcast NATURAL JOIN mediaserver.Subscribed_Podcasts
        WHERE       username = %s
        """

        r = dictfetchall(cur, sql, (username,))
        print("return val is:")
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcast subs:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (1 c)
#   Get user in progress items
#####################################################
def user_in_progress_items(username):
    """
    Get user in progress items that aren't 100%
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        ###################################################################################
        # Fill in the SQL below with a way to find all the in progress items for the user #
        ###################################################################################

        sql = """
        SELECT      media_id, play_count AS playcount, progress, lastviewed, storage_location
        FROM        mediaserver.UserMediaConsumption NATURAL JOIN mediaserver.MediaItem
        WHERE       username = %s AND progress >= 0.0 AND progress < 100.0
        """

        r = dictfetchall(cur, sql, (username,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting User Consumption - Likely no values:", sys.exc_info()[0])
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get all artists
#####################################################
def get_allartists():
    """
    Get all the artists in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        SELECT      A.artist_id, A.artist_name, count(AMD.md_id) AS count
        FROM        mediaserver.Artist A LEFT OUTER JOIN mediaserver.ArtistMetaData AMD on (A.artist_id = AMD.artist_id)
        GROUP BY    A.artist_id, A.artist_name
        ORDER BY    A.artist_name
        """

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Artists:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get all songs
#####################################################
def get_allsongs():
    """
    Get all the songs in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        SELECT      S.song_id, S.song_title, string_agg(SAA.artist_name, ', ') AS artists
        FROM        mediaserver.Song S LEFT OUTER JOIN
                    (mediaserver.Song_Artists SA INNER JOIN mediaserver.Artist a ON (SA.performing_artist_id = A.artist_id)) AS SAA  ON (S.song_id = SAA.song_id)
        GROUP BY    S.song_id, S.song_title
        ORDER BY    S.song_id
        """

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Songs:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get all podcasts
#####################################################
def get_allpodcasts():
    """
    Get all the podcasts in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        SELECT      P.*, PNEW.count as count
        FROM        mediaserver.podcast P,
                    (SELECT     P1.podcast_id, count(*) AS count
                    FROM        mediaserver.Podcast P1 LEFT OUTER JOIN mediaserver.PodcastEpisode PE USING (podcast_id)
                    GROUP BY    P1.podcast_id) PNEW
        WHERE       P.podcast_id = PNEW.podcast_id
        """

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Podcasts:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get all albums
#####################################################
def get_allalbums():
    """
    Get all the Albums in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        SELECT      A.album_id, A.album_title, ANEW.count as count, ANEW.artists
        FROM        mediaserver.Album A,
                    (SELECT     A1.album_id, count(DISTINCT AS1.song_id) AS count, array_to_string(array_agg(DISTINCT AR1.artist_name),', ') AS artists
                    FROM        mediaserver.album A1
			                    LEFT OUTER JOIN mediaserver.album_songs as1 on (a1.album_id=as1.album_id)
			                    LEFT OUTER JOIN mediaserver.song s1 on (as1.song_id=s1.song_id)
			                    LEFT OUTER JOIN mediaserver.Song_Artists sa1 on (s1.song_id=sa1.song_id)
			                    LEFT OUTER JOIN mediaserver.artist ar1 on (sa1.performing_artist_id=ar1.artist_id)
                    GROUP BY    A1.album_id) ANEW
        WHERE       A.album_id = ANEW.album_id
        """

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Albums:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (3 a,b c)
#   Get all tvshows
#####################################################
def get_alltvshows():
    """
    Get all the TV Shows in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all tv shows and episode counts #
        #############################################################################
        sql = """
        SELECT      tvshow_id, tvshow_title, COUNT(episode) AS count
        FROM        mediaserver.TVShow NATURAL JOIN mediaserver.TVEpisode
        GROUP BY    tvshow_id, tvshow_title
        ORDER BY    tvshow_id
        """

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get all movies
#####################################################
def get_allmovies():
    """
    Get all the Movies in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        SELECT      M.movie_id, M.movie_title, M.release_year, count(MIMD.md_id) AS count
        FROM        mediaserver.Movie M LEFT OUTER JOIN mediaserver.MediaItemMetaData MIMD on (M.movie_id = MIMD.media_id)
        GROUP BY    M.movie_id, M.movie_title, M.release_year
        ORDER BY    movie_id
        """

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Movies:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get one artist
#####################################################
def get_artist(artist_id):
    """
    Get an artist by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        SELECT      *
        FROM        mediaserver.Artist A LEFT OUTER JOIN
                    (mediaserver.ArtistMetaData
                    NATURAL JOIN mediaserver.MetaData
                    NATURAL JOIN mediaserver.MetaDataType) AMD ON (A.artist_id = AMD.artist_id)
        WHERE       A.artist_id = %s
        """

        r = dictfetchall(cur, sql, (artist_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Artist with ID: '" + artist_id + "'", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (2 a,b,c)
#   Get one song
#####################################################
def get_song(song_id):
    """
    Get a song by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a song    #
        # and the artists that performed it                                         #
        #############################################################################
        sql = """
        SELECT      song_title, string_agg(artist_name,', ') AS artists, length
        FROM        (mediaserver.Song S NATURAL JOIN mediaserver.Song_Artists SA)
                    INNER JOIN mediaserver.Artist A ON (SA.performing_artist_id = A.artist_id)
        WHERE       song_id = %s
        GROUP BY    song_id
        """

        r = dictfetchall(cur, sql, (song_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Songs:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (2 d)
#   Get metadata for one song
#####################################################
def get_song_metadata(song_id):
    """
    Get the meta for a song by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all metadata about a song       #
        #############################################################################

        sql = """
            SELECT DISTINCT md_value, md_type_name, song_title, mdc.md_id, mdc.md_value
            FROM mediaserver.song
            JOIN mediaserver.mediaitemmetadata mda on(song_id = media_id) LEFT JOIN mediaserver.album_songs using (song_id)
            LEFT JOIN mediaserver.album using(album_id) LEFT JOIN mediaServer.albummetadata mdb using (album_id)
            LEFT JOIN mediaserver.metadata mdc on (mda.md_id = mdc.md_id) or (mdb.md_id = mdc.md_id)
            JOIN mediaserver.metadatatype mdt using (md_type_id)
            WHERE song_id = %s;

        """

        # sql = "SELECT MDT.md_type_name, MD.md_value, MD.md_id ROM (((mediaserver.Song So JOIN mediaserver.Mediaitem MI ON (So.song_id = MI.media_id)) JOIN mediaserver.mediaitemmetadata USING (media_id)) JOIN mediaserver.metadata MD USING (md_id)) JOIN mediaserver.metadatatype MDT USING (md_type_id) WHERE So.song_id = 3940"

        r = dictfetchall(cur, sql, (song_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting song metadata for ID: " + song_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (6 a,b,c,d,e)
#   Get one podcast and return all metadata associated with it
#####################################################
def get_podcast(podcast_id):
    """
    Get a podcast by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a podcast #
        # including all metadata associated with it                                 #
        #############################################################################

        sql = """
        SELECT      podcast_id, podcast_title, podcast_uri, podcast_last_updated, md_value,md_type_id
        FROM        mediaserver.Podcast
                    NATURAL JOIN mediaserver.PodcastMetaData
                    NATURAL JOIN mediaserver.MetaData
        WHERE       podcast_id = %s
        """

        r = dictfetchall(cur, sql, (podcast_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcast with ID: " + podcast_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (6 f)
#   Get all podcast eps for one podcast
#####################################################
def get_all_podcasteps_for_podcast(podcast_id):
    """
    Get all podcast eps for one podcast by their podcast ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # podcast episodes in a podcast                                             #
        #############################################################################
        sql = """
        SELECT      media_id, podcast_episode_title, podcast_episode_uri, podcast_episode_published_date, podcast_episode_length
        FROM        mediaserver.Podcast NATURAL JOIN mediaserver.PodcastEpisode
        WHERE       podcast_id = %s
        ORDER BY    podcast_episode_published_date DESC
        """

        r = dictfetchall(cur, sql, (podcast_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Podcast Episodes for Podcast with ID: " + podcast_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (7 a,b,c,d,e,f)
#   Get one podcast ep and associated metadata
#####################################################
def get_podcastep(podcastep_id):
    """
    Get a podcast ep by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a         #
        # podcast episodes and it's associated metadata                             #
        #############################################################################

        sql = """
        SELECT      media_id, podcast_episode_title, podcast_episode_uri, podcast_episode_published_date, podcast_episode_length, md_type_name, md_value
        FROM        mediaserver.PodcastEpisode
                    NATURAL JOIN mediaserver.PodcastMetaData
                    NATURAL JOIN mediaserver.MetaData
                    NATURAL JOIN mediaserver.MetaDataType
        WHERE       media_id =  %s
        """

        r = dictfetchall(cur, sql, (podcastep_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcast Episode with ID: " + podcastep_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (5 a,b)
#   Get one album
#####################################################
def get_album(album_id):
    """
    Get an album by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about an album  #
        # including all relevant metadata                                           #
        #############################################################################
        sql = """
        SELECT      album_title, md_type_name, md_value
        FROM        mediaserver.Album
                    NATURAL JOIN mediaserver.AlbumMetaData
                    NATURAL JOIN mediaserver.Metadata
                    NATURAL JOIN mediaserver.MetaDataType
        WHERE       album_id = %s
        """

        r = dictfetchall(cur, sql, (album_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Albums with ID: " + album_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (5 d)
#   Get all songs for one album
#####################################################
def get_album_songs(album_id):
    """
    Get all songs for an album by the album ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # songs in an album, including their artists                                #
        #############################################################################
        sql = """
        SELECT      song_id, song_title, string_agg(artist_name, ', ') AS artists
        FROM        mediaserver.Album
                    NATURAL JOIN mediaserver.Album_Songs
                    NATURAL JOIN mediaserver.Song
                    NATURAL JOIN mediaserver.Song_Artists
                    INNER JOIN mediaserver.artist ON (performing_artist_id = artist_id)
        WHERE       album_id = %s
        GROUP BY    track_num, song_id, song_title
        ORDER BY    track_num
        """

        r = dictfetchall(cur, sql, (album_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Albums songs with ID: " + album_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (5 c)
#   Get all genres for one album
#####################################################
def get_album_genres(album_id):
    """
    Get all genres for an album by the album ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # genres in an album (based on all the genres of the songs in that album)   #
        #############################################################################
        sql = """
        SELECT      string_agg(DISTINCT md_value, ', ') AS songgenres
        FROM        mediaserver.MetaData MD
                    NATURAL JOIN mediaserver.MetaDataType MDT
                    INNER JOIN mediaserver.mediaitemmetadata MIMD USING (md_id)
                    INNER JOIN mediaserver.song S ON (media_id = S.song_id)
                    INNER JOIN mediaserver.album_songs ASo USING (song_id)
        WHERE       album_id = %s
        """

        r = dictfetchall(cur, sql, (album_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Albums genres with ID: " + album_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (10)
#   May require the addition of SQL to multiple
#   functions and the creation of a new function to
#   determine what type of genre is being provided
#   You may have to look at the hard coded values
#   in the sampledata to make your choices
#####################################################

def get_genre_type(genre_id):
    """
    Get all genre type by genre_id
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        sql = """
        SELECT      DISTINCT md_Type_name
        FROM        mediaserver.MetaData
                    NATURAL JOIN mediaserver.MetaDataType
                    INNER JOIN mediaserver.MediaItemMetaData USING (md_id)

        WHERE       md_id = %s
		limit 1
        """
        r = dictfetchall(cur, sql, (genre_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        print("Unexpected error getting Songs with Genre ID: " + genre_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (10)
#   Get all songs for one song_genre
#####################################################
def get_genre_songs(genre_id):
    """
    Get all songs for a particular song_genre ID in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # songs which belong to a particular genre_id                               #
        #############################################################################

        sql = """
        SELECT      DISTINCT media_id, song_title, md_value, md_type_name
        FROM        mediaserver.MetaData
                    NATURAL JOIN mediaserver.MetaDataType
                    INNER JOIN mediaserver.MediaItemMetaData USING (md_id)
                    INNER JOIN mediaserver.Song S ON (media_id = song_id)
                    INNER JOIN mediaserver.Album_Songs USING (song_id)
        WHERE       md_id = %s AND md_type_name = 'song genre'
        ORDER BY    media_id
        """

        r = dictfetchall(cur, sql, (genre_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Songs with Genre ID: " + genre_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (10)
#   Get all podcasts for one podcast_genre
#####################################################
def get_genre_podcasts(genre_id):
    """
    Get all podcasts for a particular podcast_genre ID in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # podcasts which belong to a particular genre_id                            #
        #############################################################################
        sql = """
        SELECT      DISTINCT media_id, podcast_title, md_Value, md_type_name, md_id
        FROM        mediaserver.MetaData
                    NATURAL JOIN mediaserver.MetaDataType
                    NATURAL JOIN mediaserver.MediaItemMetaData
                    NATURAL JOIN mediaserver.Podcast
                    NATURAL JOIN mediaserver.PodcastEpisode
        WHERE       md_id = %s AND md_type_name = 'podcast genre'
        ORDER BY    media_id
        """

        r = dictfetchall(cur, sql, (genre_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcasts with Genre ID: " + genre_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (10)
#   Get all movies for one film_genre
#####################################################
def get_genre_movies(genre_id):
    """
    Get all movies and tv shows for a particular film_genre ID in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # movies and tv shows which belong to a particular genre_id                 #
        #############################################################################
        sql = """
        SELECT distinct media_id, movie_title, md_value, md_type_name, md_id, movie_id
        FROM        mediaserver.MetaData
                    NATURAL JOIN mediaserver.MetaDataType
                    NATURAL JOIN mediaserver.MediaItemMetaData
                    JOIN mediaserver.Movie on (movie_id = media_id)
        WHERE       md_id = %s
        ORDER BY    movie_title
        """

        r = dictfetchall(cur, sql, (genre_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Movies and tv shows with Genre ID: " + genre_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None

#####################################################
#   Query (10)
#   Get all tv shows for one film_genre
#####################################################
def get_genre_tvshows(genre_id):
    """
    Get all movies and tv shows for a particular film_genre ID in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # movies and tv shows which belong to a particular genre_id                 #
        #############################################################################
        sql = """
            SELECT distinct tvshow_id, md_id, md_value, md_type_id, md_type_name, tvshow_title
	FROM        mediaserver.MetaData
                    NATURAL JOIN mediaserver.MetaDataType
                    NATURAL JOIN mediaserver.MediaItemMetaData
                    NATURAL JOIN mediaserver.tvshowmetadata NATURAL JOIN mediaserver.tvshow
        WHERE        md_id = %s and md_type_name = 'film genre'
        order by tvshow_title

        """

        r = dictfetchall(cur, sql, (genre_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Movies and tv shows with Genre ID: " + genre_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None

#####################################################
#   Query (4 a,b)
#   Get one tvshow
#####################################################
def get_tvshow(tvshow_id):
    """
    Get one tvshow in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a tv show #
        # including all relevant metadata       #
        #############################################################################
        sql = """
        SELECT      tvshow_title, md_type_name, md_value, md_id
        FROM        mediaserver.TVShow T
                    NATURAL JOIN mediaserver.TVShowMetaData
                    NATURAL JOIN mediaserver.MetaData
                    NATURAL JOIN mediaserver.MetaDataType
        WHERE       tvshow_id = %s
        """

        r = dictfetchall(cur, sql, (tvshow_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (4 c)
#   Get all tv show episodes for one tv show
#####################################################
def get_all_tvshoweps_for_tvshow(tvshow_id):
    """
    Get all tvshow episodes for one tv show in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # tv episodes in a tv show                                                  #
        #############################################################################
        sql = """
        SELECT      media_id, tvshow_episode_title, season, episode, air_date
        FROM        mediaserver.TVEpisode NATURAL JOIN mediaserver.TVShow
        WHERE       tvshow_id = %s
        ORDER BY    season, episode
        """

        r = dictfetchall(cur, sql, (tvshow_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get one tvshow episode
#####################################################
def get_tvshowep(tvshowep_id):
    """
    Get one tvshow episode in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        SELECT      DISTINCT T.*
        FROM        mediaserver.TVEpisode T LEFT OUTER JOIN
                    (mediaserver.MediaItemMetaData
                    NATURAL JOIN mediaserver.MetaData
                    NATURAL JOIN mediaserver.MetaDataType) TMD ON (T.media_id = TMD.media_id)
        WHERE       T.media_id = %s
        """

        r = dictfetchall(cur, sql, (tvshowep_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################

#   Get one movie
#####################################################
def get_movie(movie_id):
    """
    Get one movie in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        select *
        from mediaserver.movie m left outer join
            (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) mdt
        on (m.movie_id=mdt.media_id)
        where m.movie_id=%s;
        """

        r = dictfetchall(cur, sql, (movie_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Movies:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Find all matching tvshows
#####################################################
def find_matchingtvshows(searchterm):
    """
    Get all the matching TV Shows in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
            select
                t.*, tnew.count as count
            from
                mediaserver.tvshow t,
                (select
                    t1.tvshow_id, count(te1.media_id) as count
                from
                    mediaserver.tvshow t1 left outer join mediaserver.TVEpisode te1 on (t1.tvshow_id=te1.tvshow_id)
                    group by t1.tvshow_id) tnew
            where t.tvshow_id = tnew.tvshow_id and lower(tvshow_title) ~ lower(%s)
            order by t.tvshow_id;"""

        r = dictfetchall(cur,sql,(searchterm,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

#####################################################
#   Query (9)
#   Find all matching Movies
#####################################################
def find_matchingmovies(searchterm):
    """
    Get all the matching Movies in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about movies    #
        # that match a given search term                                            #
        #############################################################################
        sql = """
        SELECT     T.*, TNew.count AS count
        FROM       mediaserver.Movie T,
                   (SELECT      T1.movie_id, count(T2.media_id) as count
                    FROM        mediaserver.Movie T1 LEFT OUTER JOIN mediaserver.MediaItemMetaData T2 on (T1.movie_id = T2.media_id)
                    GROUP BY    T1.movie_id) TNew
        WHERE       T.movie_id = TNew.movie_id
                    AND LOWER(movie_title) ~ LOWER(%s)
        ORDER BY    T.movie_id
        """

        r = dictfetchall(cur,sql,(searchterm,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Movies:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################
#   Add a new Movie
#####################################################
def add_movie_to_db(title, release_year, description, storage_location, genre):
    """
    Add a new Movie to your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        SELECT
            mediaserver.addMovie(
                %s,%s,%s,%s,%s);
        """

        cur.execute(sql, (storage_location, description, title, release_year, genre))
        conn.commit()  # Commit the transaction
        r = cur.fetchone()
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a movie:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (8)
#   Add a new Song
#####################################################
def add_song_to_db(storage_location, description, song_title, length, song_genre, artist_name, artist_id):
    """
    Get all the matching songs in your media server
    """
    #########
    # TODO  #
    #########

    #############################################################################
    # Fill in the Function  with a query and management for how to add a new    #
    # song to your media server. Make sure you manage all constraints           #
    #############################################################################
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        sql = """
        SELECT  mediaserver.addSong(%s,%s,%s,%s,%s,%s,%s);
        """


        cur.execute(sql,(storage_location,description,song_title,length,song_genre, artist_name, artist_id))
        conn.commit()
        res = cur.fetchone()
        # res = int(res[0])
        print("return val isss:")
        print(res)
        print("retunr val over")

        cur.close()
        conn.close()
        return res
    except:
        print("Unexpected error adding song:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Find all matching songs - new
#####################################################
# required - song_id,name,category
def find_matchingsongs(searchterm,genre):
    """
    Get all the matching Songs in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database

        sql = """
        SELECT distinct s.song_id,s.song_title,s.length
        FROM mediaserver.song s JOIN mediaserver.mediaitemmetadata on (song_id = media_id)
        natural JOIN mediaserver.metadata
        natural JOIN mediaserver.metadatatype
        where lower(s.song_title) ~ lower(%s) and md_type_name = 'song genre' and lower(md_value) ~ lower(%s)
        ORDER BY s.song_id;

        """


        r = dictfetchall(cur, sql, (searchterm,genre,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All songs:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get last Movie
#####################################################
def get_last_movie():
    """
    Get all the latest entered movie in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        SELECT      MAX(movie_id) AS movie_id
        FROM        mediaserver.movie
        """

        r = dictfetchone(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a movie:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


def get_last_song():
    """
    Get all the latest entered song in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        SELECT      MAX(song_id) AS song_id
        FROM        mediaserver.song
        """

        r = dictfetchone(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a movie:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#  FOR MARKING PURPOSES ONLY
#  DO NOT CHANGE

def to_json(fn_name, ret_val):
    """
    TO_JSON used for marking; Gives the function name and the
    return value in JSON.
    """
    return {'function': fn_name, 'res': json.dumps(ret_val)}

# =================================================================
# =================================================================
def filter_matchingtvshows(air_date,searchterm,sign):
    """
    Get all the matching TV Shows in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select t.*, tnewer.count as count
                 from mediaserver.tvshow t, (select t1.tvshow_id, count(te1.media_id) as count
                            from mediaserver.tvshow t1 left outer join mediaserver.TVEpisode te1 on (t1.tvshow_id=te1.tvshow_id)
                            where te1.air_date """ + sign + """ %s
							AND te1.episode = 1 AND te1.season = 1
            				group by t1.tvshow_id) tnew, (select t10.tvshow_id, count(te10.media_id) as count
                                                          from mediaserver.tvshow t10 left outer join mediaserver.TVEpisode te10 on (t10.tvshow_id=te10.tvshow_id)
                                                          group by t10.tvshow_id) tnewer
                 where tnewer.tvshow_id = t.tvshow_id AND t.tvshow_id = tnew.tvshow_id AND SIMILARITY(tvshow_title, %s) > 0
                 order by t.tvshow_id;"""

        r = dictfetchall(cur,sql,(air_date,searchterm))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Filter TV Shows:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


def filter_matchingmovies(release_year,searchterm,sign):
    """
    Get all the matching Movies in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about movies    #
        # that match a given search term                                            #
        #############################################################################
        sql = """
        SELECT m.movie_id, m.movie_title, m.release_year
        FROM mediaserver.movie m
        WHERE release_year """ + sign + """ %s AND SIMILARITY(movie_title, %s) > 0.15
        ORDER BY m.movie_id;
        """

        r = dictfetchall(cur,sql,(release_year,searchterm))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Filter Movies:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


def filter_matchingsongs(artist_name, length, sign):
    """
    Get all the matching Movies in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about movies    #
        # that match a given search term                                            #
        #############################################################################
        sql = """
         SELECT s.song_id, s.song_Title
        FROM mediaserver.song s natural join mediaserver.song_Artists join mediaserver.artist on (performing_Artist_id = artist_id)
        WHERE s.length """ + sign + """ %s AND SIMILARITY(artist_name, %s) > 0.15
        ORDER BY s.song_id;

        """

        r = dictfetchall(cur,sql,(length,artist_name))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Filter Songs:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

def filter_matchingpodcasts(last_updated,countEp, count, sign ):
    """
    Get all the matching Movies in your media server
    """
    print(last_updated)
    print(countEp)

    print(count)
    print(sign)

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about movies    #
        # that match a given search term                                            #
        #############################################################################
        sql = """
         SELECT P.podcast_id, podcast_title, PNEW.count as count, P.podcast_last_updated
                FROM        mediaserver.podcast P,
                            (SELECT     P1.podcast_id, count(*) AS count
                            FROM        mediaserver.Podcast P1 LEFT OUTER JOIN mediaserver.PodcastEpisode PE USING (podcast_id)
                            GROUP BY    P1.podcast_id) PNEW
                WHERE       P.podcast_id = PNEW.podcast_id and PNEW.count """ + count + """ %s  AND extract(year from podcast_last_updated) """ + sign + """ %s
        """

        r = dictfetchall(cur,sql,(countEp, last_updated))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Filter Podcast:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None
