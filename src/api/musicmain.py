from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from enum import Enum
import math
import sqlalchemy
from src import database as db
from typing import Dict
from pip._vendor import requests
import json
# import openai
# import creds as creds
import os
import dotenv
from dotenv import load_dotenv, find_dotenv


router = APIRouter(
    prefix="/musicmain",
    tags=["musicmain"],
    dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    username: str

class Artist(BaseModel):
    artist_name: str

class Song(BaseModel):
    song_name: str
    artist_name: str
    featured_artist: str
    explicit_rating: float
    length: int

class Album(BaseModel):
    album_name: str
    artist_name: str
    song_list: list[Song]
    genre: str
    explicit_rating: int
    label: str
    release_date: str


# user playlist relational table: userid and playlistid and playlist name
# song playlsit user table: songid and playlistid and userid
class Playlist(BaseModel):
    playlist_name: str
    user_id: int

@router.post("/create_artist")
def create_artist(new_artist: Artist):
    """ Create new artist  """
    with db.engine.begin() as connection:
        artist_check = connection.execute(sqlalchemy.text(
            "SELECT * FROM artist WHERE artist_name = :name"),
                                        [{"name": new_artist.artist_name}]).scalar()
        if artist_check is None:
            artist_id = connection.execute(sqlalchemy.text("INSERT INTO artist (artist_name) VALUES (:name) RETURNING id"),
                                            [{"name": new_artist.artist_name}]).scalar()
        else:
            return "Artist Creation Error: Artist already exists"
    return {"Artist created! artist id": artist_id}

@router.post("/upload_music/")
def upload_new_music(new_album_catalog: Album):
    """Upload a new album including songs and metadata"""
    with db.engine.begin() as connection:
        album_check = connection.execute(sqlalchemy.text(
            "SELECT * FROM album WHERE album_name = :name"),
                                        [{"name": new_album_catalog.album_name}]).scalar()
        artistId = connection.execute(sqlalchemy.text(
            "SELECT id FROM artist WHERE artist_name = :name"),
                                        [{"name": new_album_catalog.artist_name}]).scalar()
        if album_check is None:
            albumId = connection.execute(sqlalchemy.text(
                "INSERT INTO album (album_name, artist_id, genre, explicit_rating, label, release_date) VALUES (:album_name, :artist_id, :genre, :xprat, :label, :release_date) RETURNING id"),
                    [{"album_name": new_album_catalog.album_name, "artist_id": artistId, "genre": new_album_catalog.genre, "xprat": new_album_catalog.explicit_rating, "label": new_album_catalog.label, "release_date": new_album_catalog.release_date}]).scalar()
            for song in new_album_catalog.song_list:
                connection.execute(sqlalchemy.text(
                    "INSERT INTO song (song_name, artist_id, featured_artist, explicit_rating, length, album_id) VALUES (:song_name, :artist_id, :featured_artist, :explicit_rating, :length, :album_id)"),
                        [{"song_name": song.song_name, "artist_id": artistId, "featured_artist": song.featured_artist, "explicit_rating": song.explicit_rating, "length": song.length, "album_id": albumId}])
        else:
            return "Upload Error: Album already exists"
    return f"Album: {new_album_catalog.album_name} uploaded!"


@router.post("/log_streams/")
def log_streams(song_name: str, artist_name: str, username: str):
    """   Take in a song that is logged by a user, and put it in the stream table"""

    with db.engine.begin() as connection:
        user_id = connection.execute(sqlalchemy.text("SELECT user_id FROM users WHERE username = :name"), 
                            [{"name": username}]).scalar()
        if user_id is None:
            return "User does not exist!"
        song_id = connection.execute(sqlalchemy.text("SELECT song_id FROM song JOIN artist ON artist.id = song.artist_id WHERE song_name = :name AND artist_name = :artist_name"),
                            [{"name": song_name, "artist_name": artist_name}]).scalar()
        if song_id is None:
            return "Song does not exist!"
        connection.execute(sqlalchemy.text("INSERT INTO streams (user_id, song_id) VALUES (:userID, :songID)"), 
                            [{"userID": user_id , "songID": song_id}])

    return "Song streamed!"

@router.post("/add_user/")
def add_user(user: User):
    """Add user to users table"""

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("INSERT INTO users (username) VALUES (:userName)"), 
                           [{"userName": user.username }])

    return "User added!"


@router.post("/get_total_streams/")
def get_streams(user: User):
    """Lists of all songs streamed by user"""
    output = [()]
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(""" 
                                                    SELECT song.song_name, artist.artist_name, song.featured_artist FROM streams
                                                    JOIN song on streams.song_id = song.song_id 
                                                    JOIN artist on artist.id = song.artist_id 
                                                    JOIN users on users.user_id = streams.user_id
                                                    WHERE users.user_id = :USERID
                                                                    """), [{"USERID": user.user_id}])

    if result is not None:
        for song_name, artist_name, featured_artist in result:
            output.append((song_name, artist_name))

    return output

@router.post("/get_stream_by_Artist/")
def streams_byArtist(user: User, artist: Artist):
    """Get all streams for one artist by one user"""

    output = []

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(""" 
                                                SELECT song.song_name  FROM streams
                                                JOIN song on streams.song_id = song.song_id 
                                                JOIN artist on artist.id = song.artist_id 
                                                JOIN users on users.user_id = streams.user_id
                                                WHERE users.user_id = :USERID AND artist.id = :ARTISTID
                                                                """), [{"USERID": user.user_id, "ARTISTID": artist.artist_id}])
         
    if result is not None:    
        for song in result:
            output.append({"song": song})

    return output

@router.post("/create_playlist/") 
def create_playlist(playlist_name: str, username: str):
    """Create a new playlist for a user"""
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""INSERT INTO user_playlist (playlist_name, user_id)
                                              SELECT :playlist_name, user_id
                                              FROM users where username = :username"""),
                           [{"playlist_name": playlist_name, "username": username}])
    return f"Playlist: {playlist_name} Created!"


@router.post("/add_song_to_playlist/")
def add_songs_to_playlist(song_name: str, album: str, playlist_name: str , username: str):
    """Add a song to a playlist for a user"""
    with db.engine.begin() as connection:
        song_check = connection.execute(sqlalchemy.text(
            "SELECT song_id FROM song WHERE song_name = :name"),
                                        [{"name": song_name}]).scalar()
        if song_check is not None:
            connection.execute(sqlalchemy.text(
                    """INSERT INTO song_playlist (playlist_id, song_id)
                            WITH
                            playlist_id AS (
                                SELECT
                                    playlist_id
                                FROM
                                    user_playlist
                                JOIN users ON users.user_id = user_playlist.user_id
                                WHERE
                                    users.username = :username
                                    AND user_playlist.playlist_name = :playlist_name
                            ),
                            song_id AS (
                                SELECT
                                    song.song_id
                                FROM
                                    song
                                JOIN album on album.id = song.album_id
                                WHERE
                                    song.song_name = :song_name 
                                    AND album.album_name = :album
                            )
                            SELECT
                            *
                            FROM
                            playlist_id,
                            song_id
                            """),
                        [{"song_name": song_name, "album": album, "username": username, "playlist_name": playlist_name}])
        else:
            return "Song Addition Error: Song does not exist"
    return f"Song: {song_name} Added to Playlist: {playlist_name}"

@router.post("/songs/submit_rating/")
def add_rating_to_song(song: str, user_rating: int):
    """Submits their rating for a song if it is explicit or not"""
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""INSERT INTO explicit_submissions (song_id, exbool) 
                                            SELECT song_id, :rating
                                            FROM song
                                            WHERE song_name = :thesong"""),
                           [{"thesong": song, "rating": user_rating}])
    
    return "Rating Submitted"

@router.post("/playlist/get_clean_songs/")
def get_clean_songs(playlist_name: str):
    """Returns all songs from the playlist that are not explicit"""
    filtered_arr = []
    with db.engine.begin() as connection:
        filterd_list = connection.execute(sqlalchemy.text("""SELECT song_id
                                                FROM song_playlist
                                                JOIN user_playlist on user_playlist.playlist_id = song_playlist.playlist_id
                                                WHERE user_playlist.playlist_name = :playlistName"""),
                           [{"playlistName": playlist_name}])
    
        for songs in filterd_list:
            filtered_arr.append(songs)
            
    return filtered_arr


@router.post("/songs/recommend_songs/")
def reccomend_song(genre: str):
    """Reccomends a song based on the genre given by the user"""

    APIKEY = ""



    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    APIKEY = os.environ.get("CHAT_KEY")

    # Define the endpoint URL
    url = "https://api.openai.com/v1/chat/completions"

    # Define the request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + APIKEY
    }

    # Define the request payload
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"You are a Music Reccomendation assistant, I will give you a genre name or lead, and then you will reccomend one song based on that. And you will only say the song name, and artist, nothing else\
                      Reccomend me a song that is {genre}."}],
        "temperature": 0.7
    }

    # Convert payload to JSON format
    payload_json = json.dumps(payload)

    # Make the POST request
    response = requests.post(url, headers=headers, data=payload_json)

    # Print the response
    myDict = {}
    myDict = response.json()
    myDict= myDict['choices']
    myDict = myDict[0]
    myDict = myDict['message']['content']

    
    return myDict


@router.post("/top_streams/")
def top_streams():
    """Gets the top 10 streamed songs"""
    stream_data = []
    with db.engine.begin() as connection:
        top_streams = connection.execute(sqlalchemy.text("""
                                           SELECT ROW_NUMBER() OVER (ORDER BY COUNT(streams.stream_id) DESC) AS Position,
                                                song.song_name AS Song, artist.artist_name As Artist, COUNT(streams.stream_id) AS Streams
                                           FROM streams
                                           JOIN song on song.song_id = streams.song_id
                                           JOIN artist on artist.id = song.artist_id
                                           GROUP BY streams.song_id, song.song_name, artist.artist_name
                                           ORDER BY Position ASC
                                           LIMIT 10
                                           """))
        for Position, Song, Artist, Streams in top_streams:
            stream_data.append({
                'Position': Position,
                'Song': Song,
                'Artist': Artist,
                'Streams': Streams
            })
    return stream_data

@router.post("/playlist/recommend")
def recommend_new_songs(playlist_name: str):
    """Gets the top 5 songs based on your playlist and other playlists with similar songs"""
    ret = []
    
    with db.engine.begin() as connection:
        recc_songs = connection.execute(sqlalchemy.text("""WITH
                                                            playlist_6_songs AS (
                                                                SELECT
                                                                song_id
                                                                FROM
                                                                song_playlist
                                                                JOIN user_playlist AS up ON up.playlist_id = song_playlist.playlist_id
                                                                JOIN users AS u ON u.user_id = up.user_id
                                                                WHERE
                                                                up.playlist_name = :playlist_name
                                                            ),
                                                            matching_playlists AS (
                                                                SELECT
                                                                sp.playlist_id
                                                                FROM
                                                                song_playlist AS sp
                                                                JOIN user_playlist AS up ON up.playlist_id = sp.playlist_id
                                                                JOIN users AS u ON u.user_id = up.user_id
                                                                WHERE
                                                                song_id IN (
                                                                    SELECT
                                                                    song_id
                                                                    FROM
                                                                    playlist_6_songs
                                                                )
                                                                AND up.playlist_name != :playlist_name
                                                                GROUP BY
                                                                sp.playlist_id
                                                                HAVING
                                                                COUNT(DISTINCT song_id) >= 3
                                                            )
                                                            SELECT DISTINCT
                                                            sp.song_id,
                                                            s.song_name,
                                                            al.album_name,
                                                            art.artist_name
                                                            FROM
                                                            song_playlist AS sp
                                                            JOIN song AS s ON s.song_id = sp.song_id
                                                            JOIN album AS al ON s.album_id = al.id
                                                            JOIN artist AS art ON s.artist_id = art.id
                                                            WHERE
                                                            playlist_id IN (
                                                                SELECT
                                                                playlist_id
                                                                FROM
                                                                matching_playlists
                                                            )
                                                            AND sp.song_id NOT IN (
                                                                SELECT
                                                                song_id
                                                                FROM
                                                                playlist_6_songs
                                                            )
                                                            LIMIT
                                                            5
                                                            """),
                           [{"playlist_name": playlist_name}])
        
        for songs in recc_songs:
            ret.append({
                "song_id": songs.song_id,
                "song_name": songs.song_name,
                "album_name": songs.album_name,
                "artist_name": songs.artist_name
            })
    return ret




@router.post("/remove_song_from_playlist/")
def remove_song_from_playlist(song_name: str, playlist_name: str):
    """Remove song from user playlist"""

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(
            """
                DELETE FROM song_playlist
USING user_playlist, song
WHERE song_playlist.playlist_id = user_playlist.playlist_id
  AND song_playlist.song_id = song.song_id
  AND user_playlist.playlist_name = :playlistName
  AND song.song_name = :songName
            """),
            [{"songName": song_name, "playlistName" : playlist_name }])
        
    return "SUCCESS"
