# CSE6242-Team 101 Music Discovery System project

A graduate-course project on helping music lovers discover new songs and explore the depth of our Spotify data

By Nick Ghinazzi, Anh Tran, Anupam Priyadarshi, Nathaniel Pung, Daniel Remmes, and Akshat Chauhan

## Description:

With the advent of Spotify, Pandora, Youtube and iTunes streaming services have contributed the majority of music industry revenue. Each of them provides their own methods of recommendation, but none allow for the detailed customization for a playlist that is desired. We developed an app that gives the users specific control over what characteristics are driving their playlist and which artists they see.

For our source data, we scraped the Spotify API for each year using a Python script. We chose Spotify since they bought out The Echo Nest company which was responsible for creating the Million Song Dataset.

Source code of this project is available under CODE/ folder. This app is built using python flask, sqlite db, d3, javascript, jquery, html and css. It has following directory structure within CODE folder:

## CODE:

  - data: It has all the data scrapped from spotify using API. Spotify.db is **mini dataset** that is must for this application to  run. For the **full dataset** and how to implement it, please refer to the file - CODE/data/full_dataset.txt.

  - sql: sql query for creating all the tables used for this project
  
  - static: This has all the static content used.
    css:/
    images:/
    js:/
    lib:/
  
  - templates: All the html files running for the project.
  
    *.py  - several python files - must be needed for this project to run successfully.
  
    requirements.txt - Needed for required python libraries.
  
    Dockerfile - Needed to containerize the app.
    
## Installation:

To setup and run this app locally, please follow below steps. If you would like to skip local installation and directly want to use the app, please use the amazon AWS hosted website as:
http://ec2-3-92-57-132.compute-1.amazonaws.com

### Pre-requisites:

1. Python version 3.7.7 and above (run command python -v to check the version. Python version needs to be upgraded otherwise.)
2. git (optional if you want to directly doanload zip and run the app. Required if source needs to be cloned from git repo).

For mac users:
```
1. Download team101final.zip and unzip it or git clone https://github.gatech.edu/apriyadarshi7/team101final.git 
2. Navigate to the directory where unzipped the above folder using terminal by typing command "cd team101final"
3. cd CODE
4. python -m venv venv
5. source venv/bin/activate
6. pip install -r requirements.txt
7. export FLASK_APP=app.py
8. flask run
```
For window users:
```
1. Download team101final.zip and unzip it or git clone https://github.gatech.edu/apriyadarshi7/team101final.git 
2. Navigate to the directory where unzipped the above folder using command line. command line can be opened on window PC by using [Windows key] + [R] then type in "cmd" and hit [enter]. Once command line is open, run command "cd team101final"
3. cd CODE
4. python -m venv venv
5. .\venv\Scripts\activate.bat
6. pip install -r requirements.txt
7. set FLASK_APP=app.py
8. flask run
```
The app should be available on http://localhost:5000 once above commands are successfully executed.

### Execution:

Once the application is accessible using http://localhost:5000, please use the credentials to login. Login credentials are userid/password is project_team_101/cse6242. Please ensure you login, certain pages will not work if the user is not logged in first.

Once successfully logged in, user can navigate to pages using index page. The user interface of this application encompasses tseparate sections that the users can access via the homepage. The  sections are: Discover, Explore, Vizualize, About, and Login/Logout

1. Discover: This page allows the user to search for any song, select the features that are important to them, and the system will find similar songs for the user to try out using the preview. The user can then decide if they like the reccomendation or not and mark the song as such, which will inform future reccomendations. This page uses HTML/Javascript/CSS and Python/Flask with a SQLite database. 
Once on discover page, please follow below steps:
  - Search for a song: e.g. type "ab" etc to pull the list of songs.
  - Select upto 3 features
  - Click discover songs, this will pull the songs from various clusters.
  - Listen to sample songs from the list.
  - Like/Unlike song(s)
  - Get more of like/unliked songs - This will improvise the cluster score and pull the songs from nearest cluster of the liked song.
  - View Cluster - This will provide the n-dimensional view of the clusters for features selected.

2. Explore: This page allows users to explore the entire dataset by selecting the song attributes that they care about. There are six different attributes to filter on, and a search function that automatically filters the results as the user types. This page uses HTML/Javascript/CSS and Python/Flask with a SQLite database.
  Once on explore page, please follow below steps:
    - Select Year to pull the specific songs for that year
    - Select and vary tempo, energy, mood, liveness, danceability combinations to pull the songs for specific year or Any year>=1950
    - Samples can be played.
    
3. Vizualize: This pages uses Tableau to generate vizualizations of the data. The user can use the interactive dashboard to filter for their preference and see the generated graphs. This page uses HTML/Javascript/CSS and Python/Flask with a SQLite database , and also uses the Tableau engine to generate the vizualizations. For the full-dataset dashboard, you can open the Tableau link in: **CODE/Templates/visualization_tableau_link.txt**

Below is the link to access the Tableau dashboard:
https://public.tableau.com/views/spotify_15863656936800/Dashboard1?:language=en-US&:display_count=n&:origin=viz_share_link

4. About - This page has details of the project and installation instruction documented.

5. Login/Logout - This page faciliates user login and logout. We store the user data in sqlite db for authentication and once authenticated that user data is stored in session.

6. Some features we were not able to incorporate onto the webpage yet.  This includes the node/edge graph for artist to artist relationship and the node/edge graph of the artist's genre. To view these relationship please go to https://poloclub.github.io/argo-graph-lite/ and load the snapshot files below:

  - CODE/data/artist_relationship_argolite_snapshot.txt
  - CODE/data/artist_genre_argolite_snapshot.txt 
  - Please remember these take up a lot of RAM and may require a high performance PC to load it. Other options include using Gephi software to load and view the graph.
