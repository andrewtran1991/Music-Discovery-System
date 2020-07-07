from dataclasses import dataclass
from flask import Flask, url_for, redirect, render_template, request, abort, g, jsonify, session, flash
from flask_login import LoginManager, login_user , logout_user , current_user , login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'data/spotify.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS=True

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_ECHO'] = SQLALCHEMY_ECHO
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY']="secret-key"

db = SQLAlchemy(app)

@dataclass
class spotify(db.Model):
    row_counter = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.String(80), unique=True, nullable=False)
    song_name = db.Column(db.String(80))
    # artist_id = db.Column(db.String(80))
    artist_name = db.Column(db.String(80))
    # album_id = db.Column(db.String(120), unique=True, nullable=False)
    # track_number = db.Column(db.String(120))
    album_name = db.Column(db.String(120))
    # uri = db.Column(db.String(120))
    track_href = db.Column(db.String(250))
    tempo = db.Column(db.Float)
    mode = db.Column(db.Integer)
    loudness = db.Column(db.Float)
    speechiness = db.Column(db.Float)
    liveness = db.Column(db.Float)
    valence = db.Column(db.Float)
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    acousticness = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    artist_genres = db.Column(db.String(300))
    artist_popularity = db.Column(db.Integer)
    album_popularity = db.Column(db.Integer)
    sp_album_release_date_year = db.Column(db.Integer)

    def __repr__(self):
        return '<spotify %r>' % self.song_name

    def serialize(self):
        return {
            'row_counter':self.row_counter,
            'song_id': self.song_id, 
            'song_name': self.song_name,
            'album_name': self.album_name,
            'artist_name': self.artist_name,
            'track_href':self.track_href,
            'tempo': self.tempo,
            'energy': self.energy,
            'liveness': self.liveness, 
            'danceability': self.danceability,
            'valence': self.valence,
            'acousticness': self.acousticness,
            'instrumentalness':self.instrumentalness,
            'artist_genres':self.artist_genres, 
            'artist_popularity':self.artist_popularity,
            'album_popularity':self.album_popularity,
            'year':self.sp_album_release_date_year
        }


@dataclass
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self , username,email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def check_password(self, password):
        if self.password_hash==password:
            return True
        else:
            return False

    def __repr__(self):
        return '<User {}>'.format(self.username, self.email, self.password_hash)

@dataclass
class User_to_song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    song_id = db.Column(db.String, db.ForeignKey('spotify.song_id'))
    like_count = db.Column(db.Integer)
    dislike_count = db.Column(db.Integer)

    def __init__(self , user_id,song_id, like_count, dislike_count):
        self.user_id = user_id
        self.song_id = song_id
        self.like_count = like_count
        self.dislike_count = dislike_count

    def __repr__(self):
        return '<User_to_song {}>'.format(self.user_id, self.song_id, self.like_count, self.dislike_count)