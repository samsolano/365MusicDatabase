from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from enum import Enum
import math
import sqlalchemy
from src import database as db
from typing import Dict


router = APIRouter(
    prefix="/musicmain",
    tags=["musicmain"],
    dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    user_id: int
    username: str

class Artist(BaseModel):
    artist_id: int
    artist_name: str

class Song(BaseModel):
    song_id: int
    song_name: str
    artist_name: str
    featured_artist: str
    explicit_rating: float
    length: int
class Album(BaseModel):
    album_name: str
    song_list: list[Song]
    artist_id: str
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
    



@router.post("/upload_music/")
def upload_new_music(new_album_catalog: Album):
    """Upload a new album including songs and metadata"""
    with db.engine.begin() as connection:
        album_check = connection.execute(sqlalchemy.text(
            "SELECT * FROM album WHERE album_name = :name"),
                                        [{"name": new_album_catalog.album_name}]).scalar()
        if album_check is None:
            connection.execute(sqlalchemy.text(
                "INSERT INTO album (album_name, artist_id, genre, explicit_rating, label, release_date) VALUES (:album_name, :artist_id, :genre, :xprat, :label, :release_date)"),
                    [{"album_name": new_album_catalog.album_name, "artist_id": new_album_catalog.artist_id, "genre": new_album_catalog.genre, "xprat": new_album_catalog.explicit_rating, "label": new_album_catalog.label, "release_date": new_album_catalog.release_date}])
            for song in new_album_catalog.song_list:
                connection.execute(sqlalchemy.text(
                    "INSERT INTO album (song_name, artist_id, featured_artist, explicit_rating, length) VALUES (:song_name, :artist_id, :featured_artist, :explicit_rating, :length)"),
                        [{"song_name": song.song_name, "artist_id": 1, "featured_artist": song.featured_artist, "explicit_rating": song.explicit_rating, "length": song.length}])
        else:
            return "Upload Error: Album already exits"
    return "OK"



@router.post("/log_streams/")
def log_streams(song: Song, user: User):
    """   take in a song that is logged by a user, and put it in the stream table"""

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("INSERT INTO streams (user_id, song_id) VALUES (:userID, :songID)"), 
                           [{"userID": user.user_id , "songID": song.song_id}])

    return "OK"

@router.post("/add_user/")
def add_user(user: User):
    """add user to users table"""

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("INSERT INTO users (username) VALUES (:userName)"), 
                           [{"userName": user.username }])

    return "OK"


@router.post("/get total streams/")
def get_streams(user: User):
    """returns list of all songs streamed by user"""
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(""" 
                                                    SELECT songs.song_name, artists.artist_name, songs.featured_artist FROM streams
                                                    JOIN songs on streams.song_id = songs.song_id 
                                                    JOIN artists on artists.id = songs.artist_id 
                                                    WHERE users.user_id = :USERID
                                                                    """), [{"USERID": user.user_id}])

    return result

@router.post("/get_stream_byArtist/")
def streams_byArtist(user: User, artist: Artist):
    """add user to users table"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(""" 
                                                SELECT songs.song_name  FROM streams
                                                JOIN songs on streams.song_id = songs.song_id 
                                                JOIN artists on artists.id = songs.artist_id 
                                                WHERE users.user_id = :USERID AND artists.artist_id = :ARTISTID
                                                                """), [{"USERID": user.user_id, "ARTISTID": artist.artist_id}])

    return result



@router.get("/create_playlist/") 
def create_playlist(playlist: Playlist):
    """Create a new playlist for a user"""
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("INSERT INTO user_playlist (playlist_name, user_id) VALUES (:playlist_name, :user_id)"),
                           [{"playlist_name": playlist.playlist_name, "user_id": playlist.user_id}])
    return "Playlist Created"


@router.get("/add_song_to_playlist/")
def add_song_to_playlist(song: Song, playlist: Playlist, user: User):
    """Add a song to a playlist for a user"""
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("INSERT INTO song_playlist (song_id, playlist_id, user_id) VALUES (:song_id, :playlist_id, :user_id)"),
                           [{"song_id": song.song_id, "playlist_id": playlist.playlist_id, "user_id": user.user_id}])
    return "Song Added to Playlist"

    
    
    # work right here ma boi
    
    
    
    
    
    """
    Search for cart line items by customer name and/or potion sku.

    Customer name and potion sku filter to orders that contain the 
    string (case insensitive). If the filters aren't provided, no
    filtering occurs on the respective search term.

    Search page is a cursor for pagination. The response to this
    search endpoint will return previous or next if there is a
    previous or next page of results available. The token passed
    in that search response can be passed in the next search request
    as search page to get that page of results.

    Sort col is which column to sort by and sort order is the direction
    of the search. They default to searching by timestamp of the order
    in descending order.

    The response itself contains a previous and next page token (if
    such pages exist) and the results as an array of line items. Each
    line item contains the line item id (must be unique), item sku, 
    customer name, line item total (in gold), and timestamp of the order.
    Your results must be paginated, the max results you can return at any
    time is 5 total line items.
    """

    return {
        "previous": "",
        "next": "",
        "results": [
            {
                "line_item_id": 1,
                "item_sku": "1 oblivion potion",
                "customer_name": "Scaramouche",
                "line_item_total": 50,
                "timestamp": "2021-01-01T00:00:00Z",
            }
        ],
    }