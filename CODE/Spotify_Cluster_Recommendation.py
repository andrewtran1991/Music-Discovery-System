import pandas as pd
import random
from sklearn.cluster import KMeans
from sklearn import preprocessing
import time
import sqlite3
from flask import jsonify
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib
from os.path import join, dirname, realpath
from base64 import b64encode
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

pd.set_option('display.max_columns', None)
matplotlib.use('Agg')
# UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/images/cluster_3d.png')

# num_clusters = 5
# cluster_score = [10] * num_clusters
# To do:
# Get features from user (Return features[])
# def add_features(feat):
#     features.append(feat)


# Create cols for query
def create_query_col(feat_list):
    std_columns = ['song_id', 'song_name', 'artist_name', 'artist_popularity']
    cols = std_columns + feat_list

    return cols


# Import data
def get_data(cols):
    select = ', '.join(f'{i}' for i in cols)
    # Insert location of spotify.db file
    conn = sqlite3.connect("data/spotify.db")
    # Need to determine how much of data to include based on artist popularity
    q = "Select " + select + " from spotify order by song_id"
    spot_data = pd.read_sql_query(q, conn)
    conn.close()

    return spot_data

# Get suggestions (Return song_id):
def get_song_id(spot_data, artist, song_title):
    song_id = spot_data[(spot_data['artist_name'] == artist) & (spot_data['song_name'] == song_title)]['song_id']
    return song_id.iloc[0]

# Get song parameters
def get_song_parameters(spot_data, song_id, features):
    values = spot_data[spot_data['song_id'] == song_id][features]
    return values


# Filter data (feature_vals[] return dataset_filtered)
def filter_data(df, features, song_id, parameters):

    feature_max = []
    feature_min = []

    for x in parameters:

        # Provide minimum values for data if feature = 0
        if df[df['song_id'] == song_id][x].iloc[0] == 0:
            feature_max.append(0.14)
            feature_min.append(0.075)
        else:
            feature_max.append(df[df['song_id'] == song_id][x].iloc[0] * 1.4)
            feature_min.append(df[df['song_id'] == song_id][x].iloc[0] * 0.75)

    # create query for filtering
    where = ' & '.join(f'{i}>{j}' for i, j in zip(features, feature_min))
    where1 = ' & '.join(f'{i}<{j}' for i, j in zip(features, feature_max))

    where2 = where1 + ' & ' + where

    out = df.query(where2)

    return out


# Create clusters in dataset (dataset_filtered return dataset_filtered[cluster_id], cluster_scoring[equal])
def create_clusters(df, features_picked, k, features):

    x = df[features_picked].values  # returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    x_df = pd.DataFrame(x_scaled, columns=features)[features_picked]

    clusters = KMeans(k).fit(x_df)

    ids = clusters.labels_
    df = pd.DataFrame(df)
    df['cluster_id'] = ids

    return clusters, df


# Recommend songs (cluster_scoring[equal] return 10_song_list)
def recommend_songs(df, cluster_scoring,num_clusters):

    cluster_per = []
    tot = sum(cluster_scoring)

    # get percentages
    for j in range(num_clusters):
        cluster_per.append(cluster_scoring[j]/tot)

    # get cumulative values
    cu = 0
    cluster_cum = []
    for n in range(num_clusters):
        cu += cluster_per[n] * 1000000
        cluster_cum.append(cu)

    cluster_picked = []
    # Testing random picking
    for i in range(10):
        rand = random.sample(range(1000000), 1)[0]
        picked = False
        for k in range(len(cluster_cum)):
            if cluster_cum[k] >= rand and picked == False:
                cluster_picked.append(int(k))
                picked = True

    # Create song list
    song_list = []
    for song_num in range(10):
        song_list.append(df[df['cluster_id'] == cluster_picked[song_num]].sample()['song_id'].iloc[0])

    return song_list


# Receive feedback (df, dict with 1/-1, previous cluster score, num clusters)
def feedback(df, songs_dict, cluster_score_t, num_clusters):

    c_score = cluster_score_t
    scores = [0] * num_clusters

    for song in songs_dict:
        # print(song)
        song_data = df[df['song_id'] == song]
        c_id = int(song_data['cluster_id'].iloc[0])
        scores[c_id] += songs_dict[song]

    for s in range(num_clusters):
        c_score[s] += scores[s]

    return c_score


# Suggest 10 new songs (cluster_scoring[adjusted] return 10_song_list)
# Repeat
# Suggest Final 10 Song list
def final_songs(df, cluster_score_t,num_clusters):
    final_song_list = recommend_songs(df, cluster_score_t,num_clusters)
    final_df = df[df.song_id.isin(final_song_list)]

    return final_df[['song_name', 'artist_name', 'cluster_id']]

##############################################################
# User inputs
# Selected Features
features = ['tempo', 'danceability', 'energy', 'liveness']

# Creating Query
cols = create_query_col(features)

# Get Data
data = get_data(cols)

# Picking Song Name (from db)
# song_name = ''
# artist_name = ''
# song_id=''


###############################################################

# Set up data
# Get Song ID
# song_id = get_song_id(data, artist_name, song_name)
# print('Song: ', song_name, ' by ', artist_name)
# print('song id: ', song_id)
# print()

# Get parameters
# parameters = get_song_parameters(data, song_id, features)
# print(parameters)
# print()

# # Get filtered data
# data_filtered = filter_data(data, features, song_id)

# print('Original Data Size: ', data.shape)
# print('Filtered Data Size: ', data_filtered.shape)

# Create clusters in dataset (dataset_filtered return dataset_filtered[cluster_id], cluster_scoring[equal])
# Need to determine best number of clusters
# num_clusters = 5
# cluster, data_filtered = create_clusters(data_filtered, features, num_clusters)

# # Creating the base cluster scoring
# cluster_score = [10] * num_clusters


###############################################################################
# Main program (Continue until satisfied with suggestions)
# cont = True

# while cont == True:

#     print('Starting Cluster Score: ', cluster_score)
#     songs = recommend_songs(data_filtered, cluster_score)
#     cluster_score = feedback(data_filtered, songs, cluster_score)
#     print('New Scores: ', cluster_score)

#     cont_resp = input('Continue (Y/N): ')
#     if cont_resp == 'Y':
#         cont = True
#     else:
#         cont = False

# print()
# print('Final Cluster Score: ', cluster_score)
# print()
# print('Final Suggestions: ')
# print(final_songs(data_filtered, cluster_score))

# Recommend songs (cluster_scoring[equal] return 10_song_list)
#   Equal percentage of all clusters
# Receive feedback (10_song_list, song_scores return cluster_scores[], song_list)
# Adjust cluster scores(cluster_scores return cluster_scoring[adjusted]
# Suggest 10 new songs (cluster_scoring[adjusted] return 10_song_list)
# Repeat

def get_filtered_data(song_id, features):
    cols = create_query_col(features)
    data = get_data(cols)
    parameters = get_song_parameters(data, song_id, features)
    data_filtered = filter_data(data, features, song_id, parameters)
    # print('Original Data Size: ', data.shape)
    # print('Filtered Data Size: ', data_filtered.shape)
    return data_filtered


def get_recommendation(song_id, features, num_clusters, cluster_score):
    print("song_id: ", song_id)
    print("no of clusters: ", num_clusters)
    print("cluster_score: ", cluster_score)
    data_filtered = get_filtered_data(song_id, features)
    cluster, data_filtered = create_clusters(data_filtered, features, num_clusters,features)
    songs = recommend_songs(data_filtered, cluster_score,num_clusters)
    return songs, data_filtered


def get_feedback(liked_dict, data_filtered, init_recommended_songs, num_clusters, cluster_score):
    print("liked_dict: ", liked_dict)
    print("no of clusters: ", num_clusters)
    print("cluster_score: ", cluster_score)
    revised_score = feedback(data_filtered, liked_dict, cluster_score,num_clusters)
    print("revised cluster score after like/unlike: ",revised_score)
    return revised_score


def get_recommendation_with_feedback(liked_dict,data_filtered, init_recommended_songs, num_clusters, cluster_score):
    try:
        # print("liked_dict: ", liked_dict)
        # print("no of clusters: ", num_clusters)
        songs = recommend_songs(data_filtered, cluster_score,num_clusters)
        return songs
    except:
        return init_recommended_songs



def radar_cluster(features, data_filtered, cluster_score):

    # get sorted cluster scores
    sorted_cluster_score = list(np.argsort(cluster_score)[::-1][:len(cluster_score)])

    # scale df for radar chart
    x = data_filtered[features].values  # returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    x_df = pd.DataFrame(x_scaled, columns=features)[features]
    clusters = data_filtered['cluster_id'].tolist()
    x_df['cluster_id'] = clusters

    #set labels
    favorites = ['Favorite Profile', '2nd Favorite Profile', '3rd Favorite Profile', '4th Favorite Profile'
        , '5th Favorite Profile', '6th Favorite Profile', '7th Favorite Profile']

    fig = go.Figure()

    for i in range(len(cluster_score)):

        fig.add_trace(go.Scatterpolar(
            r=x_df[x_df['cluster_id'] == sorted_cluster_score[i]][features].mean(),
            theta=features,
            fill='toself',
            name=favorites[i]
        ))

    fig.update_layout(
        title="Song Feature Profile Preferences",
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="#000000"
        ),

        showlegend = True
    )

    # fig.show()
    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
    return graphJSON

def plot_3D(df, feat, cluster_score):

    if (len(feat)== 1):
        return
    colours = ['blue', 'red', 'green', 'purple', 'orange', 'cyan', 'deeppink']

    favorites = ['Favorite Profile', '2nd Favorite Profile', '3rd Favorite Profile', '4th Favorite Profile'
        , '5th Favorite Profile', '6th Favorite Profile', '7th Favorite Profile']

    sorted_cluster_score = list(np.argsort(cluster_score)[::-1][:len(cluster_score)])

    # plot 3D
    if len(feat) == 3:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for i in range(0, len(cluster_score)):
            cluster_df = df[df['cluster_id'] == sorted_cluster_score[i]]
            ax.scatter(
                cluster_df[feat[0]].mean(),
                cluster_df[feat[1]].mean(),
                cluster_df[feat[2]].mean(),
                color=colours[i],
                alpha=0.5,
                label=favorites[i]

            )

        ax.set_xlabel(feat[0])
        ax.set_ylabel(feat[1])
        ax.set_zlabel(feat[2])
        ax.legend(loc='best', bbox_to_anchor=(1, 0.5))
        plt.subplots_adjust(left=0.0, right=0.65)

        fig.suptitle('Song Feature Profile Preference', fontsize=16)

    # Plot 2D
    if len(feat) == 2:
        fig = plt.figure()
        ax = plt.subplot(111)

        for i in range(0, len(cluster_score)):
            cluster_df = df[df['cluster_id'] == sorted_cluster_score[i]]
            plt.scatter(
                cluster_df[feat[0]].mean(),
                cluster_df[feat[1]].mean(),
                color=colours[i],
                alpha=0.5,
                label=favorites[i]
            )

        plt.xlabel('tempo')
        plt.ylabel('energy')
        plt.title('Clusters')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.subplots_adjust(right=0.65)

    #plt.show()

    # plt.show()
    # plt.savefig(UPLOADS_PATH)
    output = BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(output)
    plot_data= b64encode(output.getvalue()).decode('ascii')
    output.seek(0)
    return plot_data
