from flask_app import app, limiter
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from lyricsgenius import Genius
import os
import time
import twilio
from twilio.rest import Client

lyrics_genius_token = os.environ.get("LYRICS_GENIUS_TOKEN")
lyrics_genius_client_secret = os.environ.get("LYRICS_GENIUS_CLIENT_SECRET")
genius = Genius(lyrics_genius_token)

twilio_account_SID = os.environ.get("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
my_twilio_num = os.environ.get("MY_TWILIO_NUM")

genius = Genius(lyrics_genius_token)

string_regex = "[^A-Za-z0-9]+"


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/song_a_gram", methods=['POST'])
@limiter.limit("5 per day")
def song_a_gram():
    if not User.is_valid(request.form):
        return redirect("/")

    session['your_name'] = request.form['your_name'].title()
    session['friend_name'] = request.form['friend_name'].title()
    session['artist'] = request.form['artist'].title()
    session['song_title'] = request.form['song_title'].title()
    session['friend_number'] = "+1" + request.form['friend_number']

    if session['artist'] == "Ghost":
        session['artist'] = "Ghost BC"

    artist = genius.search_artist(session['artist'], max_songs=3, sort="title")
    print(artist.songs)

    song = artist.song(session['song_title'])
    song_lyrics = song.lyrics.replace("Embed", "")

    artist.add_song(song)
    print(song_lyrics)

    client = Client(twilio_account_SID, twilio_auth_token)

    message = client.messages \
        .create(
            body=f"Hi {session['friend_name']}, \n{session['your_name']} sent you a lyric Song-a-gram!\n\n{song_lyrics[:1200]}",
            from_=my_twilio_num,
            to=session['friend_number']
        )

    print(message.sid)

    time.sleep(2)

    message2 = client.messages.create(
        body=f"{song_lyrics[1200:2799:]}",
        from_=my_twilio_num,
        to=session['friend_number']
    )

    time.sleep(2)

    message3 = client.messages.create(
        body=f"{song_lyrics[2799:]}",
        from_=my_twilio_num,
        to=session['friend_number']
    )
    print(message2.sid)
    print(message2.status)

    return redirect("/results")


@app.route("/results")
def results():
    return render_template("results.html")
