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
import creds as creds


router = APIRouter(
    prefix="/musicmain",
    tags=["musicmain"],
    dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    user_id: int
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
    playlist_id: int
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
    return {"artist_id": artist_id}

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
    return "OK"


@router.post("/log_streams/")
def log_streams(song_id: int, user: User):
    """   take in a song that is logged by a user, and put it in the stream table"""

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("INSERT INTO streams (user_id, song_id) VALUES (:userID, :songID)"), 
                           [{"userID": user.user_id , "songID": song_id}])

    return "OK"

@router.post("/add_user/")
def add_user(user: User):
    """add user to users table"""

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("INSERT INTO users (username) VALUES (:userName)"), 
                           [{"userName": user.username }])

    return "OK"


@router.post("/get_total_streams/")
def get_streams(user: User):
    """returns list of all songs streamed by user"""
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

@router.post("/get_stream_byArtist/")
def streams_byArtist(user: User, artist: Artist):
    """get all streams for one artist by one user"""

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
def create_playlist(playlist: Playlist):
    """Create a new playlist for a user"""
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("INSERT INTO user_playlist (playlist_name, user_id) VALUES (:playlist_name, :user_id)"),
                           [{"playlist_name": playlist.playlist_name, "user_id": playlist.user_id}])
    return "Playlist Created"


@router.post("/add_song_to_playlist/")
def add_song_to_playlist(song: Song, playlist: Playlist, user: User):
    """Add a song to a playlist for a user"""
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("INSERT INTO song_playlist (song_id, playlist_id, user_id) VALUES (:song_id, :playlist_id, :user_id)"),
                           [{"song_id": song.song_id, "playlist_id": playlist.playlist_id, "user_id": user.user_id}])
    if(song.song_id is None or playlist.playlist_id is None or user.user_id is None):
        return "Error: Song, Playlist, or User does not exist"
    else:
            "Song Added to Playlist"

@router.post("/songs/submit_rating/")
def add_rating_to_song(song: str, user_rating: int):
    """Submits their rating for a song if it is explicit or not"""
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""INSERT INTO explicit_submissions (songid, exbool) 
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
    """Gets a genre and reccomends a song based on that"""

    # Define the endpoint URL
    url = "https://api.openai.com/v1/chat/completions"

    # Define the request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + creds.OPENAI_API_KEY
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