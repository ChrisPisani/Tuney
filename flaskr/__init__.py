import os
import sys
import pickle
import json
import time
from flask import Flask, flash, render_template, request, redirect
from forms import Song_search
from genius import Genius
from lyrics import Lyrics
from results import generate_results_data


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        app.config['SECRET_KEY'] = os.urandom(24)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        app.config['SECRET_KEY'] = os.urandom(24)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/home', methods=['GET', 'POST'])
    def home():
        # Song_search is the form from forms.py where all the form data is stored
        search = Song_search(request.form)
        if request.method == 'POST':
            # this calls the results template and genius API from genius.py/GetLyrics
            return search_results(search)

        return render_template('home.html', form=search)

    @app.route('/results')
    def search_results(search):
        genius = Genius()
        # this is the stored value for dropdown either: Song Name or Song Name & Artist
        search_type = search.data['select']
        # Name of the song to search for
        song_string = search.data['song_string']
        artist_string = ""
        # If user is searching by Song & Artist, store a value in artist_string
        if search_type == "Song Name & Artist":
            artist_string = search.data['artist_string']

        # GetLyrics is the genius/bs4 call to get lyrics from genius.py
        results = genius.get_lyrics(song_string, artist_string)
        # if results exist, render the page and information, else flash on home page "no results"
        if results is not None:
            data = generate_results_data(song_string, artist_string, genius, results)

            return render_template('results.html',
                                   lyrics=data[0],
                                   songTitle=data[1],
                                   artistName=data[2],
                                   album_img=data[3],
                                   emotions=data[4])
        flash('No results found!', 'error')
        return redirect('/home')

    return app
