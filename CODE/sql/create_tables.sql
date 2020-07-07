CREATE TABLE User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL
);
INSERT INTO User (username,email ,password_hash) VALUES('anupam','anupam@xyz.com', 'abcd');
INSERT INTO User (username,email ,password_hash) VALUES('admin','admin@xyz.com', 'password');
INSERT INTO User (username,email ,password_hash) VALUES('project_team_101','apriyadarshi7@gatech.edu', 'cse6242');

DROP TABLE User_to_song;

CREATE TABLE User_to_song (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    song_id TEXT NOT NULL,
    like_count INTEGER NOT NULL,
    dislike_count INTEGER NOT NULL,
    FOREIGN KEY (user_id) 
      REFERENCES User (id) 
         ON DELETE CASCADE 
         ON UPDATE NO ACTION,
    FOREIGN KEY (song_id) 
      REFERENCES spotify (song_id) 
         ON DELETE CASCADE 
         ON UPDATE NO ACTION
);

INSERT INTO User_to_song (user_id,song_id,like_count,dislike_count) VALUES(1,'2dCgZocKF09Hn2WpuDp5Li', 1, 0);

select User.username, spotify.song_name, spotify.artist_name,User_to_song.like_count from User, User_to_song, spotify where User.Id = User_to_song.user_id and User_to_song.song_id=spotify.row_counter;

--TOY DB CREATION
--must update table name
--https://stackoverflow.com/questions/6037675/how-to-randomly-delete-20-of-the-rows-in-a-sqlite-table
DELETE FROM table WHERE random() > 5534023222112865485
VACUUM;
--run it a few times until select count(*) is around 100,000

DELETE FROM spotify WHERE tempo=0;
--big dataset has only 3972 which skews the results if selected as a 'liked' song