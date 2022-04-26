"""
Route management.

This provides all of the websites routes and handles what happens each
time a browser hits each of the paths. This serves as the interaction
between the browser and the database while rendering the HTML templates
to be displayed.

You will have to make
"""

# Importing the required packages
from modules import *
from flask import *
import database

user_details = {}                   # User details kept for us
session = {}                        # Session information (logged in state)
page = {}                           # Determines the page information

# Initialise the application
app = Flask(__name__)
app.secret_key = """U29tZWJvZHkgb25jZSB0b2xkIG1lIFRoZSB3b3JsZCBpcyBnb25uYSBy
b2xsIG1lIEkgYWluJ3QgdGhlIHNoYXJwZXN0IHRvb2wgaW4gdGhlIHNoZWQgU2hlIHdhcyBsb29r
aW5nIGtpbmRhIGR1bWIgV2l0aCBoZXIgZmluZ2VyIGFuZCBoZXIgdGh1bWIK"""


#####################################################
#   INDEX
#####################################################

@app.route('/')
def index():
    """
    Provides the main home screen if logged in.
        - Shows user playlists
        - Shows user Podcast subscriptions
        - Shows superUser status
    """
    # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'User Management'

    # Get a list of user playlists
    user_playlists = None
    user_playlists = database.user_playlists(user_details['username'])
    # Get a list of subscribed podcasts
    user_subscribed_podcasts = None
    user_subscribed_podcasts = database.user_podcast_subscriptions(user_details['username'])
    # Get a list of in-progress items
    user_in_progress_items = None
    user_in_progress_items = database.user_in_progress_items(user_details['username'])
    # Data integrity checks
    if user_playlists == None:
        user_playlists = []

    if user_subscribed_podcasts == None:
        user_subscribed_podcasts = []

    if user_in_progress_items == None:
        user_in_progress_items = []

    return render_template('index.html',
                           session=session,
                           page=page,
                           user=user_details,
                           playlists=user_playlists,
                           subpodcasts=user_subscribed_podcasts,
                           usercurrent=user_in_progress_items)

#####################################################
#####################################################
####    User Management
#####################################################
#####################################################

#####################################################
#   LOGIN
#####################################################

@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    Provides /login
        - [GET] If they are just viewing the page then render login page.
        - [POST] If submitting login details, check login.
    """
    # Check if they are submitting details, or they are just logging in
    if(request.method == 'POST'):
        # submitting details
        # The form gives back EmployeeID and Password
        login_return_data = database.check_login(
            request.form['username'],
            request.form['password']
        )

        # If it's null, saying they have incorrect details
        if login_return_data is None:
            page['bar'] = False
            flash("Incorrect username/password, please try again")
            return redirect(url_for('login'))

        # If there was no error, log them in
        page['bar'] = True
        flash('You have been logged in successfully')
        session['logged_in'] = True

        # Store the user details for us to use throughout
        global user_details
        user_details = login_return_data[0]

        return redirect(url_for('index'))

    elif(request.method == 'GET'):
        return(render_template('login.html', session=session, page=page))


#####################################################
#   LOGOUT
#####################################################

@app.route('/logout')
def logout():
    """
    Logs out of the current session
        - Removes any stored user data.
    """
    session['logged_in'] = False
    page['bar'] = True
    flash('You have been logged out')
    return redirect(url_for('index'))

#####################################################
#####################################################
####    List All items
#####################################################
#####################################################


#####################################################
#   List Artists
#####################################################
@app.route('/list/artists')
def list_artists():
    """
    Lists all the artists in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Artists'

    # Get a list of all artists from the database
    allartists = None
    allartists = database.get_allartists()

    # Data integrity checks
    if allartists == None:
        allartists = []


    return render_template('listitems/listartists.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allartists=allartists)


#####################################################
#   List Songs
#####################################################
@app.route('/list/songs')
def list_songs():
    """
    Lists all the songs in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Songs'

    # Get a list of all songs from the database
    allsongs = None
    allsongs = database.get_allsongs()




    # Data integrity checks
    if allsongs == None:
        allsongs = []


    return render_template('listitems/listsongs.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allsongs=allsongs)

#####################################################
#   List Podcasts
#####################################################
@app.route('/list/podcasts')
def list_podcasts():
    """
    Lists all the podcasts in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List podcasts'

    # Get a list of all podcasts from the database
    allpodcasts = None
    allpodcasts = database.get_allpodcasts()

    # Data integrity checks
    if allpodcasts == None:
        allpodcasts = []


    return render_template('listitems/listpodcasts.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allpodcasts=allpodcasts)


#####################################################
#   List Movies
#####################################################
@app.route('/list/movies')
def list_movies():
    """
    Lists all the movies in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Movies'

    # Get a list of all movies from the database
    allmovies = None
    allmovies = database.get_allmovies()


    # Data integrity checks
    if allmovies == None:
        allmovies = []


    return render_template('listitems/listmovies.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allmovies=allmovies)


#####################################################
#   List Albums
#####################################################
@app.route('/list/albums')
def list_albums():
    """
    Lists all the albums in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Albums'

    # Get a list of all Albums from the database
    allalbums = None
    allalbums = database.get_allalbums()


    # Data integrity checks
    if allalbums == None:
        allalbums = []


    return render_template('listitems/listalbums.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allalbums=allalbums)


#####################################################
#   List TVShows
#####################################################
@app.route('/list/tvshows')
def list_tvshows():
    """
    Lists all the tvshows in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List TV Shows'

    # Get a list of all tvshows from the database
    alltvshows = None
    alltvshows = database.get_alltvshows()


    # Data integrity checks
    if alltvshows == None:
        alltvshows = []


    return render_template('listitems/listtvshows.html',
                           session=session,
                           page=page,
                           user=user_details,
                           alltvshows=alltvshows)




#####################################################
#####################################################
####    List Individual items
#####################################################
#####################################################

#####################################################
#   Individual Artist
#####################################################
@app.route('/artist/<artist_id>')
def single_artist(artist_id):
    """
    Show a single artist by artist_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'Artist ID: '+artist_id

    # Get a list of all artist by artist_id from the database
    artist = None
    artist = database.get_artist(artist_id)

    # Data integrity checks
    if artist == None:
        artist = []

    return render_template('singleitems/artist.html',
                           session=session,
                           page=page,
                           user=user_details,
                           artist=artist)


#####################################################
#   Individual Song
#####################################################
@app.route('/song/<song_id>')
def single_song(song_id):
    """
    Show a single song by song_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'Song'

    # Get a list of all song by song_id from the database
    song = None
    song = database.get_song(song_id)
    print("PRINTING SONGS NOW:")
    print(song)

    songmetadata = None
    songmetadata = database.get_song_metadata(song_id)
    print("PRINTING SONGSMETAAA NOW:")
    print(songmetadata)


    # Data integrity checks
    if song == None:
        song = []

    if songmetadata == None:
        songmetadata = []

    return render_template('singleitems/song.html',
                           session=session,
                           page=page,
                           user=user_details,
                           song=song,
                           songmetadata=songmetadata)

#####################################################
#   Query (6)
#   Individual Podcast
#####################################################
@app.route('/podcast/<podcast_id>')
def single_podcast(podcast_id):
    """
    Show a single podcast by podcast_id in your media server
    Can do this without a login
    """
    #########
    # TODO  #
    #########

    #############################################################################
    # Fill in the Function below with to do all data handling for a podcast     #
    #############################################################################

    page['title'] = 'Podcast Details' # Add the title

    # Set up some variables to manage the returns from the database fucntions
    details = None
    details = database.get_podcast(podcast_id)
    # podcast = database.get_podcast(podcast_id)

    temp3 = []

    for i in range(len(details)):
        temp3.append(list(details[i].values()))

    for i in range(len(details)):
        details[i].pop('podcast_id')

    temp4 =[]
    for i in range(len(details)):
        temp4.append(list(details[i].values()))
    md = ["No Copyright Holder Information found.", None, None]


    for i in range(len(temp4)):

        if temp4[i][4] == 5:
            md[0] = temp4[i][3]
        elif temp4[i][4] == 4:
            md[1] = temp4[i][3]
        else:
            md[2] = temp4[i][3]

    for i in range(len(temp4)):
        temp4[i].pop(4)
        md.append(temp4[i][3])

    for i in range(len(temp4)):
        temp4[i].append(md)
        temp4[i].pop(3)

    deets = {}
    for i in range(len(temp3)):
        deets[temp3[i][0]]=temp4[i]

    #----------------------------------------------------------------
    # Once retrieved, do some data integrity checks on the data
    podcast = None
    podcast = database.get_all_podcasteps_for_podcast(podcast_id)
    #
    # podcastEpi = None
    # podcastEpi = get_all_podcasteps_for_podcast(podcast_id)



    # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES


    temp = []

    for i in range(len(podcast)):
    	temp.append(list(podcast[i].values()))

    for i in range(len(podcast)):
        podcast[i].pop('media_id')

    temp2 =[]
    for i in range(len(podcast)):
    	temp2.append(list(podcast[i].values()))


    dict = {}
    for i in range(len(temp)):
        dict[temp[i][0]]=temp2[i]

    return render_template('singleitems/podcast.html',
                           session=session,
                           page=page,
                           user=user_details, result=dict, info=deets, podcast = podcast)

#####################################################
#   Query (7)
#   Individual Podcast Episode
#####################################################
@app.route('/podcastep/<media_id>')
def single_podcastep(media_id):
    """
    Show a single podcast epsiode by media_id in your media server
    Can do this without a login
    """
    #########
    # TODO  #
    #########
    podcastep = database.get_podcastep(media_id)
    edit_podcastep = database.get_podcastep(media_id)
    for i in range(len(edit_podcastep)):
    	edit_podcastep[i]["md_value"] = edit_podcastep[i]["md_value"].strip("<p></p>")
    if len(edit_podcastep) > 0:
        edit_podcastep = edit_podcastep[:1]




    #############################################################################
    # Fill in the Function below with to do all data handling for a podcast ep  #
    #############################################################################

    page['title'] =  podcastep[0].get('podcast_episode_title')# Add the title

    # Set up some variables to manage the returns from the database fucntions

    # Once retrieved, do some data integrity checks on the data

    # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
    return render_template('singleitems/podcastep.html',
                           session=session,
                           page=page,
                           user=user_details, podcastep = podcastep, edited = edit_podcastep)


#####################################################
#   Individual Movie
#####################################################
@app.route('/movie/<movie_id>')
def single_movie(movie_id):
    """
    Show a single movie by movie_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Movies'

    # Get a list of all movies by movie_id from the database
    movie = None
    movie = database.get_movie(movie_id)


    # Data integrity checks
    if movie == None:
        movie = []


    return render_template('singleitems/movie.html',
                           session=session,
                           page=page,
                           user=user_details,
                           movie=movie)


#####################################################
#   Individual Album
#####################################################
@app.route('/album/<album_id>')
def single_album(album_id):
    """
    Show a single album by album_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Albums'

    # Get the album plus associated metadata from the database
    album = None
    album = database.get_album(album_id)

    album_songs = None
    album_songs = database.get_album_songs(album_id)

    album_genres = None
    album_genres = database.get_album_genres(album_id)

    # Data integrity checks
    if album_songs == None:
        album_songs = []

    if album == None:
        album = []

    if album_genres == None:
        album_genres = []

    return render_template('singleitems/album.html',
                           session=session,
                           page=page,
                           user=user_details,
                           album=album,
                           album_songs=album_songs,
                           album_genres=album_genres)


#####################################################
#   Individual TVShow
#####################################################
@app.route('/tvshow/<tvshow_id>')
def single_tvshow(tvshow_id):
    """
    Show a single tvshows and its eps in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'TV Show'

    # Get a list of all tvshows by tvshow_id from the database
    tvshow = None
    tvshow = database.get_tvshow(tvshow_id)

    tvshoweps = None
    tvshoweps = database.get_all_tvshoweps_for_tvshow(tvshow_id)

    # Data integrity checks
    if tvshow == None:
        tvshow = []

    if tvshoweps == None:
        tvshoweps = []

    return render_template('singleitems/tvshow.html',
                           session=session,
                           page=page,
                           user=user_details,
                           tvshow=tvshow,
                           tvshoweps=tvshoweps)

#####################################################
#   Individual TVShow Episode
#####################################################
@app.route('/tvshowep/<tvshowep_id>')
def single_tvshowep(tvshowep_id):
    """
    Show a single tvshow episode in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List TV Shows'

    # Get a list of all tvshow eps by media_id from the database
    tvshowep = None
    tvshowep = database.get_tvshowep(tvshowep_id)


    # Data integrity checks
    if tvshowep == None:
        tvshowep = []


    return render_template('singleitems/tvshowep.html',
                           session=session,
                           page=page,
                           user=user_details,
                           tvshowep=tvshowep)

#####################################################
#   Query (10)
#   Individual Genre
#####################################################
@app.route('/genre/<genre_id>')
def single_genre(genre_id):
    """
    Show a single genre in your media server
    First, figure out what type of genre this is
    Then list all items that have that genre:
    1. Song Genre
        a. list all songs
    2. Film Genre
        a. list all tv shows and films
    3. Postcast Genre
        a. list all podcasts
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    #########
    # TODO  #
    #########
    type = database.get_genre_type(genre_id)
    print("----------")
    print(type)
    media = []
    media2 = []
    if type[0]['md_type_name'] == "song genre":
        media = database.get_genre_songs(genre_id)


    elif type[0]['md_type_name'] == "film genre":
        media = database.get_genre_movies(genre_id)
        media2 = database.get_genre_tvshows(genre_id)
        print(media)

    elif type[0]['md_type_name'] == "podcast genre":
        media = database.get_genre_podcasts(genre_id)
        print((media))

    #############################################################################
    # Fill in the Function below with to do all data handling for a genre       #
    #############################################################################

    page['title'] = '' # Add the title

    # Identify the type of genre - you may need to add a new function to database.py to do this

    # Set up some variables to manage the returns from the database functions
    #   There are some function frameworks provided for you to do this.

    # Once retrieved, do some data integrity checks on the data

    # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
    return render_template('singleitems/genre.html',
                           session=session,
                           page=page,
                           user=user_details, instance=media, instance2 = media2, genre = media[0]['md_value'], id = genre_id)


#####################################################
#####################################################
####    Search Items
#####################################################
#####################################################

#####################################################
#   Search Songs
#####################################################
@app.route('/search/song', methods=['POST','GET'])
def search_song():
    """
    Search all the songs in your media server
    """

    # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'Song Search'

    # Get a list of matching tv shows from the database
    song = None
    if(request.method == 'POST'):

        song = database.find_matchingsongs(request.form['searchterm'])

    # Data integrity checks
    if song == None or song == []:
        song = []
        page['bar'] = False
        flash("No matching songs found, please try again")
    else:
        page['bar'] = True
        flash('Found '+str(len(song))+' results!')
        session['logged_in'] = True

    return render_template('searchitems/search_song.html',
                           session=session,
                           page=page,
                           user=user_details,
                           song=song)







#####################################################
#   Search TVShow
#####################################################
@app.route('/search/tvshow', methods=['POST','GET'])
def search_tvshows():
    """
    Search all the tvshows in your media server
    """

    # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'TV Show Search'

    # Get a list of matching tv shows from the database
    tvshows = None
    if(request.method == 'POST'):

        tvshows = database.find_matchingtvshows(request.form['searchterm'])

    # Data integrity checks
    if tvshows == None or tvshows == []:
        tvshows = []
        page['bar'] = False
        flash("No matching tv shows found, please try again")
    else:
        page['bar'] = True
        flash('Found '+str(len(tvshows))+' results!')
        session['logged_in'] = True

    return render_template('searchitems/search_tvshows.html',
                           session=session,
                           page=page,
                           user=user_details,
                           tvshows=tvshows)

#####################################################
#   Query (9)
#   Search Movie
#####################################################
@app.route('/search/movie', methods=['POST','GET'])
def search_movies():
    """
    Search all the movies in your media server
    """
    # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    #########
    # TODO  #
    #########

    #############################################################################
    # Fill in the Function below with to do all data handling for searching for #
    # a movie                                                                   #
    #############################################################################

    page['title'] = '' # Add the title
    movies = None
    if(request.method == 'POST'):

        movies = database.find_matchingmovies(request.form['searchterm'])

    # Data integrity checks
    if movies == None or movies == []:
        movies = []
        page['bar'] = False
        flash("No matching tv shows found, please try again")
    else:
        page['bar'] = True
        flash('Found '+str(len(movies))+' results!')
        session['logged_in'] = True

    if request.method == 'POST':
        # Set up some variables to manage the post returns

        # Once retrieved, do some data integrity checks on the data

        # Once verified, send the appropriate data to

        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES or Go elsewhere
        return render_template('searchitems/search_movies.html',
                    session=session,
                    page=page,
                    user=user_details, movies= movies)
    else:
        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
        return render_template('searchitems/search_movies.html',
                           session=session,
                           page=page,
                           user=user_details)
#####################################################
#   Add Movie
#####################################################
@app.route('/add/movie', methods=['POST','GET'])
def add_movie():
    """
    Add a new movie
    """
    # # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'Movie Creation'

    movies = None
    print("request form is:")
    newdict = {}
    print(request.form)

    # Check your incoming parameters
    if(request.method == 'POST'):

        # verify that the values are available:
        if ('movie_title' not in request.form):
            newdict['movie_title'] = 'Empty Film Value'
        else:
            newdict['movie_title'] = request.form['movie_title']
            print("We have a value: ",newdict['movie_title'])

        if ('release_year' not in request.form):
            newdict['release_year'] = '0'
        else:
            newdict['release_year'] = request.form['release_year']
            print("We have a value: ",newdict['release_year'])

        if ('description' not in request.form):
            newdict['description'] = 'Empty description field'
        else:
            newdict['description'] = request.form['description']
            print("We have a value: ",newdict['description'])

        if ('storage_location' not in request.form):
            newdict['storage_location'] = 'Empty storage location'
        else:
            newdict['storage_location'] = request.form['storage_location']
            print("We have a value: ",newdict['storage_location'])

        if ('film_genre' not in request.form):
            newdict['film_genre'] = 'drama'
        else:
            newdict['film_genre'] = request.form['film_genre']
            print("We have a value: ",newdict['film_genre'])

        if ('artwork' not in request.form):
            newdict['artwork'] = 'https://user-images.githubusercontent.com/24848110/33519396-7e56363c-d79d-11e7-969b-09782f5ccbab.png'
        else:
            newdict['artwork'] = request.form['artwork']
            print("We have a value: ",newdict['artwork'])

        print('newdict is:')
        print(newdict)

        #forward to the database to manage insert
        movies = database.add_movie_to_db(newdict['movie_title'],newdict['release_year'],newdict['description'],newdict['storage_location'],newdict['film_genre'])


        max_movie_id = database.get_last_movie()[0]['movie_id']

        print(max_movie_id)
        if movies is not None:
            max_movie_id = movies[0]

        # ideally this would redirect to your newly added movie
        return single_movie(max_movie_id)
    else:
        return render_template('createitems/createmovie.html',
                           session=session,
                           page=page,
                           user=user_details)


#####################################################
#   Query (8)
#   Add song
#####################################################
@app.route('/add/song', methods=['POST','GET'])
def add_song():
    """
    Add a new Song
    """
    # # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'Song Creation'

    songs = None
    print("request form is:")
    newdict = {}
    mediastuff = {}
    art = {}
    des = {}
    genre = {}
    media = []
    print(request.form)

    # Check your incoming parameters
    if(request.method == 'POST'):

        # verify that the values are available:
        if ('song_title' not in request.form):
            newdict['song_title'] = 'Empty song Value'
        else:
            newdict['song_title'] = request.form['song_title']
            print("We have a value: ",newdict['song_title'])

        if ('length' not in request.form):
            newdict['length'] = '0'
        else:
            newdict['length'] = request.form['length']
            print("We have a value: ",newdict['length'])

        if ('artist_id' not in request.form):
            newdict['artist_id'] = '0'
        else:
            newdict['artist_id'] = request.form['artist_id']
            print("We have a value: ",newdict['artist_id'])


        if ('storage_location' not in request.form):
            newdict['storage_location'] = 'Empty storage location'
        else:
            newdict['storage_location'] = request.form['storage_location']
            print("We have a value: ",newdict['storage_location'])

        if ('song genre' not in request.form):
            genre['md_type_name'] = 'song genre'
            genre['md_value'] = 'No Genre available'
            media.append(genre)

        else:
            genre['md_type_name'] = 'song genre'
            genre['md_value'] = request.form['song genre']
            media.append(genre)
            mediastuff['song genre'] = request.form['song genre']
            print("We have a value: ",mediastuff['song genre'])

        if ('description' not in request.form):
            des['md_type_name'] = 'Description'
            des['md_value'] =  'No Description available'
            mediastuff['description'] =  'No Description available'
            media.append(des)
        else:
            des['md_type_name'] = 'Description'
            des['md_value'] =  request.form['description']
            media.append(des)
            mediastuff['description'] = request.form['description']
            print("We have a value: ",mediastuff['description'])

        if ('artists' not in request.form):
            newdict['artists'] = 'No artist name available'
        else:
            newdict['artists'] = request.form['artists']
            print("We have a value: ",newdict['artists'])

        if ('artwork' not in request.form):
            art['md_type_name'] = 'artwork'
            art['md_value'] =  'No Artwork available'
            media.append(art)
            mediastuff['artwork'] =  'No Artwork available'
        else:
            art['md_type_name'] = 'artwork'
            art['md_value']  = request.form['artwork']
            mediastuff['artwork'] = request.form['artwork']

            print("We have a value: ",mediastuff['artwork'])
            media.append(art)

        print('newdict is:')
        print(newdict)

        print("media is:")
        print(media)

        print()
        str = media[0]['md_value']
        s = str.split(",")
        media.pop(0)
        for i in range(len(s)):
            dict = {'md_type_name' : 'song genre', 'md_value': s[i]}
            media.append(dict)


        #forward to the database to manage insert
        songs = database.add_song_to_db(newdict['storage_location'],mediastuff['description'], newdict['song_title'],newdict['length'],mediastuff['song genre'], newdict['artists'],newdict['artist_id'])
        max_song_id = database.get_last_song()[0]['song_id']
        print()
        print("MAX SONG ID:")
        print(max_song_id)
        print()
        print("SONGS: ")
        print(songs)
        if songs is not None:
            songs = max_song_id
            ls = []
            ls.append(newdict)
            return render_template('singleitems/song.html',
                           session=session,
                           page=page,
                           user=user_details, song = ls, songmetadata = media)
    else:
        return render_template('createitems/createsong.html',
                           session=session,
                           page=page,
                           user=user_details)
#####################################################
#   Filter TVShow
#####################################################
@app.route('/filter/tvshow', methods=['POST','GET'])
def filter_tvshows():
    """
    Filter all the tvshows in your media server
    """

    # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'TV Show Filter'
    signdict = {'equal to':'=', 'greater than':'>', 'less than':'<', 'greater than or equal to':'>=', 'less than or equal to':'<='}

    # Get a list of matching tv shows from the database
    tvshows = None
    if(request.method == 'POST'):
        print(signdict[request.form['Comparator']] + " " + request.form['air_date'])
        tvshows = database.filter_matchingtvshows(request.form['air_date'],request.form['tvshows_title'],signdict[request.form['Comparator']])

    # Data integrity checks
    if tvshows == None or tvshows == []:
        tvshows = []
        page['bar'] = False
        flash("No matching tv shows found, please try again")
    else:
        page['bar'] = True
        flash('Found '+str(len(tvshows))+' Result' + ('s' if len(tvshows) != 1 else '') + '!')
        session['logged_in'] = True

    return render_template('searchitems/filter_tvshows.html',
                           session=session,
                           page=page,
                           user=user_details,
                           tvshows=tvshows)
#####################################################
#   Filter Movie
#####################################################
@app.route('/filter/movie', methods=['POST','GET'])
def filter_movies():
    """
    Filter all the movies in your media server
    """
    # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))
    page['title'] = 'Filter movies' # Add the title
    d = {'equal to':'=', 'greater than':'>', 'less than':'<', 'greater than or equal to':'>=', 'less than or equal to':'<='}

    if request.method == 'POST':
        # Set up some variables to manage the post returns
        movies = None
        movies = database.filter_matchingmovies(request.form['release_year'],request.form['movie_title'], d[request.form['Comparator']])
        # Once retrieved, do some data integrity checks on the data
        if movies == None:
            movies = []
            page['bar'] = False
            flash("No matching movies found, please try again")
        else:
            page['bar'] = True
            flash('Found '+str(len(movies))+' Result' + ('s' if len(movies) != 1 else '') + '!')
            session['logged_in'] = True
        return render_template('searchitems/filter_movies.html',
                    session=session,
                    page=page,
                    user=user_details,
                    movies=movies)
    else:
        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
        return render_template('searchitems/filter_movies.html',
                           session=session,
                           page=page,
                           user=user_details)
############################################################################
#####3#####################FILTERING SONGS
###########################################################################3
@app.route('/filter/songs', methods=['POST','GET'])
def filter_songs():
    """
    Filter all the songs in your media server
    """
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))
    page['title'] = 'Filter Songs' # Add the title
    d = {'equal to':'=', 'greater than':'>', 'less than':'<', 'greater than or equal to':'>=', 'less than or equal to':'<='}

    if request.method == 'POST':
        # Set up some variables to manage the post returns
        songs = None
        songs = database.filter_matchingsongs(request.form['artist_name'],request.form['length'], d[request.form['Comparator']])
        # Once retrieved, do some data integrity checks on the data
        if songs == None:
            songs = []
            page['bar'] = False
            flash("No matching songs found, please try again")
        else:
            page['bar'] = True
            flash('Found '+str(len(songs))+' Result' + ('s' if len(songs) != 1 else '') + '!')
            session['logged_in'] = True
        # Once verified, send the appropriate data to

        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES or Go elsewhere
        return render_template('searchitems/filter_songs.html',
                    session=session,
                    page=page,
                    user=user_details,
                    songs=songs)
    else:
        return render_template('searchitems/filter_songs.html',
                           session=session,
                           page=page,
                           user=user_details)

        #############################################################################
        #                            filter podcasts                                #
        #############################################################################
@app.route('/filter/podcasts', methods=['POST','GET'])
def filter_podcasts():
    """
    Filter all the podcast in your media server
    """
    # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))


    page['title'] = 'Filter Podcasts' # Add the title
    d = {'equal to':'=', 'greater than':'>', 'less than':'<', 'greater than or equal to':'>=', 'less than or equal to':'<='}
    c = {'equal to':'=', 'greater than':'>', 'less than':'<', 'greater than or equal to':'>=', 'less than or equal to':'<='}

    if request.method == 'POST':
        # Set up some variables to manage the post returns
        podcasts = None
        podcasts = database.filter_matchingpodcasts(request.form['last_updated'],request.form['countEp'],c[request.form['count']], d[request.form['Comparator']])
        # Once retrieved, do some data integrity checks on the data
        if podcasts == None:
            podcasts = []
            page['bar'] = False
            flash("No matching podcasts found, please try again")
        else:
            page['bar'] = True
            flash('Found '+str(len(podcasts))+' Result' + ('s' if len(podcasts) != 1 else '') + '!')
            session['logged_in'] = True
        # Once verified, send the appropriate data to

        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES or Go elsewhere
        return render_template('searchitems/filter_podcasts.html',
                    session=session,
                    page=page,
                    user=user_details,
                    podcasts=podcasts)
    else:
        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
        return render_template('searchitems/filter_podcasts.html',
                           session=session,
                           page=page,
                           user=user_details)
