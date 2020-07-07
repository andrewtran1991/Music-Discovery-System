#!venv/bin/python
import os
import sqlite3
import pandas as pd
import json
from flask import Flask, url_for, redirect, render_template, request, Response, abort, g, jsonify, session, flash
from flask_login import LoginManager, login_user , logout_user , current_user , login_required
from flask_babel import Babel, _, lazy_gettext as _l
from datetime import datetime
from flask_bootstrap import Bootstrap
from  sqlalchemy.sql.expression import func
from models import app, db, DATABASE, User, spotify, User_to_song
from forms import LoginForm, SearchForm
from helper import Serializer
import Spotify_Cluster_Recommendation  as recommend
from collections import defaultdict

select_query = 'select song_name, song_id as sample, artist_name, tempo, loudness, mode, speechiness, liveness, valence, danceability, energy, acousticness, instrumentalness, artist_popularity, album_popularity, sp_album_release_date_year from spotify'
select_query_1 = 'select song_name, artist_name, tempo, valence from spotify'
select_query_2 = "select sp_album_release_date_year as year, count(*) as count, avg(tempo) as tempo, avg(loudness) as loudness, avg(mode) as mode, avg(speechiness) as speechiness, avg(liveness) as liveness, avg(valence) as valence, avg(danceability) as danceability, avg(energy) as energy, avg(duration_ms) as duration_ms, avg(acousticness) as acousticness, avg(instrumentalness) as instrumentalness, avg(artist_popularity) as artist_popularity, avg(album_popularity) as album_popularity  from spotify group by year"
select_query_3 = 'SELECT row_counter, song_id, song_name, artist_name, track_href FROM spotify ORDER BY RANDOM() LIMIT 10'
query_limit=' LIMIT 2000'

login_manager = LoginManager()
login_manager.init_app(app)
bootstrap = Bootstrap()
bootstrap.init_app(app)
babel = Babel()
babel.init_app(app)

like_score_dict=defaultdict(int)
data_filtered=None
initial_songs_recommended=None
num_clusters = 7
cluster_score = [10] * num_clusters
features_selected=None

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/get_songs',methods=['GET', 'POST'])
def get_songs():
    query =  select_query+ query_limit
    df = pd.read_sql(query, get_db())
    return df


@app.route('/get_songs_by_year_1/<year>',methods=['GET', 'POST'])
def get_songs_by_year_1(year):
    df =  spotify.query.filter_by(sp_album_release_date_year=int(year)).limit(2000).all()
    return json.dumps(df, cls=Serializer)

@app.route('/get_songs_by_year/<year>',methods=['GET', 'POST'])
def get_songs_by_year(year):
    if (year !='Any'):
        query =  select_query+' where sp_album_release_date_year = '+year+ query_limit
    else:
        query =  select_query+query_limit
    df = pd.read_sql(query, get_db())
    json_data = df.to_json(orient='records')
    return json_data

@app.route('/get_songs_by_year_tempo/<year>/<tempo>',methods=['GET', 'POST'])
def get_songs_by_year_tempo(year, tempo):
    query =  select_query+' where sp_album_release_date_year = '+year+ ' and tempo <='+tempo+ query_limit
    df = pd.read_sql(query, get_db())
    json_data = df.to_json(orient='records')
    return json_data

@app.route('/get_songs_by_year_energy/<year>/<energy>',methods=['GET', 'POST'])
def get_songs_by_year_energy(year, energy):
    query =  select_query+' where sp_album_release_date_year = '+year+ ' and energy <='+energy+ query_limit
    df = pd.read_sql(query, get_db())
    json_data = df.to_json(orient='records')
    return json_data

@app.route('/get_songs_by_year_valence/<year>/<valence>',methods=['GET', 'POST'])
def get_songs_by_year_valence(year, valence):
    query =  select_query+' where sp_album_release_date_year = '+year+ ' and valence <='+valence+ query_limit
    df = pd.read_sql(query, get_db())
    json_data = df.to_json(orient='records')
    return json_data

@app.route('/get_songs_by_year_liveness/<year>/<liveness>',methods=['GET', 'POST'])
def get_songs_by_year_liveness(year, liveness):
    query =  select_query+' where sp_album_release_date_year = '+year+ ' and liveness <='+liveness+ query_limit
    df = pd.read_sql(query, get_db())
    json_data = df.to_json(orient='records')
    return json_data

@app.route('/get_songs_by_year_danceability/<year>/<danceability>',methods=['GET', 'POST'])
def get_songs_by_year_danceability(year, danceability):
    query =  select_query+' where sp_album_release_date_year = '+year+ ' and valence <='+danceability+ query_limit
    df = pd.read_sql(query, get_db())
    json_data = df.to_json(orient='records')
    return json_data

@app.route('/get_songs_by_all_criteria/<year>/<tempo>/<energy>/<valence>/<liveness>/<danceability>',methods=['GET', 'POST'])
def get_songs_by_all_criteria(year,tempo,energy,valence,liveness,danceability):
    query =  select_query
    if (year !='Any'):
        query=query+' where sp_album_release_date_year = '+year
    else:
        query=query+' where sp_album_release_date_year >= '+'1950'
    if (float(tempo)>0.0):
        query=query+' and tempo <= '+tempo
    if (float(energy)>0.0):
        query=query+' and energy <= '+energy
    if(float(valence)>0.0):
        query=query+' and valence <= '+valence
    if(float(liveness)>0.0):
        query=query+' and liveness <= '+liveness
    if(float(danceability)>0.0):
        query=query+' and danceability <= '+danceability
    # print(query)
    df = pd.read_sql(query, get_db())
    json_data = df.to_json(orient='records')
    return json_data

@app.route('/get_avg_summary_stats',methods=['GET', 'POST'])
def get_avg_summary_stats():
    query =  select_query_2
    df = pd.read_sql(query, get_db())
    json_data = df.to_json(orient='records')
    return json_data

@app.route('/discover',methods=['GET', 'POST'])
def discover():
    form = SearchForm(request.form)
    return render_template("discover.html",form=form)

@app.route('/autocomplete',methods=['GET','POST'])
def autocomplete():
    search = request.args.get('q')
    search = "%{}%".format(search)
    songs = spotify.query.filter(spotify.song_name.like(search)).all()
    song_list = [{"song_id":song.song_id, "song_name":song.song_name} for song in songs]
    return jsonify(json_list=song_list)

@app.route('/like/<song_id>')
def like(song_id):
    global like_score_dict
    print('User %s liked %s'  % (current_user.username, song_id))
    found = User_to_song.query.filter_by(user_id=current_user.id, song_id=song_id).first()
    like_count=0
    if found !=None:
        found.like_count+=1
        like_count=found.like_count
        db.session.commit()
    else:
        s = User_to_song(current_user.id, song_id, 1, 0)
        like_count=s.like_count
        db.session.add(s)
        db.session.commit()
    like_score_dict[song_id]=1
    return 'liked'


@app.route('/unlike/<song_id>')
def unlike(song_id):
    global like_score_dict
    print('User %s unliked %s'  % (current_user.username, song_id))
    found = User_to_song.query.filter_by(user_id=current_user.id, song_id=song_id).first()
    dislike_count=0
    if found !=None:
        found.dislike_count+=1
        dislike_count=found.dislike_count
        db.session.commit()
    else:
        s = User_to_song(current_user.id, song_id, 0, 1)
        dislike_count=s.dislike_count
        db.session.add(s)
        db.session.commit()
    like_score_dict[song_id]=-1
    return 'unliked'

@app.route('/get_songs_for_recommendation')
def get_songs_for_recommendation():
    songlist = spotify.query.join(User_to_song,spotify.song_id==User_to_song.song_id)\
                    .filter(User_to_song.user_id==current_user.id).all()
    return "songs_for_recommendation"

@app.route('/recommend_song/<song_id>')
def recommend_song(song_id):
    song = spotify.query.filter_by(song_id=song_id).first()
    return song.serialize()

@app.route('/discover_songs/<song_id>/<features>')
def discover_songs(song_id, features):
    global data_filtered
    global initial_songs_recommended
    global like_score_dict
    global cluster_score
    global num_clusters
    global features_selected
    like_score_dict=defaultdict(int)
    num_clusters = 7
    cluster_score = [10] * num_clusters
    feature_list= json.loads(features)
    features_selected = feature_list
    initial_songs_recommended, data_filtered = recommend.get_recommendation(song_id, feature_list, num_clusters, cluster_score)
    songs=[spotify.query.filter_by(song_id=id).first().serialize() for id in initial_songs_recommended]
    return jsonify(songs)

@app.route('/get_similar_songs/<song_id>/<features>')
def get_similar_songs(song_id, features):   
    global data_filtered
    global initial_songs_recommended
    global like_score_dict
    global cluster_score
    global num_clusters
    global features_selected
    # num_clusters = 5
    # cluster_score = [10] * num_clusters
    feature_list= json.loads(features)
    features_selected=feature_list
    cluster_score = recommend.get_feedback(like_score_dict,data_filtered,initial_songs_recommended, num_clusters, cluster_score)
    revised_recommnded_songs = recommend.get_recommendation_with_feedback(like_score_dict,data_filtered,initial_songs_recommended,num_clusters,cluster_score)
    songs=[spotify.query.filter_by(song_id=id).first().serialize() for id in revised_recommnded_songs]
    like_score_dict = defaultdict(int)
    # like_score_dict.clear()
    return jsonify(songs)

@app.route('/plot_cluster',methods=['GET','POST'])
def plot_cluster():
    global data_filtered
    global cluster_score
    global features_selected
    graphJSON= recommend.radar_cluster(features_selected,data_filtered,cluster_score)
    cluster_3d_data = recommend.plot_3D(data_filtered,features_selected,cluster_score)
    return render_template("view_cluster.html",graphJSON=graphJSON, cluster_3d_data =cluster_3d_data)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title=_('Sign In'), form=form)
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/about',methods=['GET', 'POST'])
@login_required
def about():
    return render_template('about.html')

@app.route('/home',methods=['GET', 'POST'])
@login_required
def home():
    return render_template('index.html')

@app.route('/explore',methods=['GET', 'POST'])
@login_required
def explore():
    return render_template('explore.html')

@app.route('/visualize',methods=['GET', 'POST'])
@login_required
def visualize():
    return render_template('visualization_tableau.html')

if __name__ == '__main__':
    app.run(debug=True)
    
