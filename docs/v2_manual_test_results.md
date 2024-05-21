# Workflow 1

Kendrick has been looking for a place to be able to log all of his song streaming info in one easy place. So he came to us to start logging his streams.
He first uses GET /streams and then he is gonna see all of the songs he has streamed, the number of times, the artist.
He then is curious about how many times he has streamed Stevie's music so he calls GET /streams by artist. He first updates with all of the songs
that he has been listening to so that the database is up to date. Then he calls check streams to see that it has all been updated. Then he calls the get streams by artist and passes in Stevie's name and then the amount of songs streamed of Stevie's music are returned as an int.

# Testing results

<Repeated for each step of the workflow>
1.  The curl statement called.

curl -X 'POST' \
 'http://127.0.0.1:8000/musicmain/log_streams/?song_id=1' \
 -H 'accept: application/json' \
 -H 'access_token: donutHolesApiKey' \
 -H 'Content-Type: application/json' \
 -d '{
"user_id": 1,
"username": "string"
}'

2. The response received.

List of songs streamed with song name, artist name, and featured artist[]



# Workflow 2
Drake is big fan of Rap music. He wants to make a compilation of the greatest diss tracks ever made. To do so, he needs to make a playlist. Drake needs to:
    - start by calling POST /playlist/newplaylist and give his playlist a name. He chooses to name it Rap Beef.
    - then Drake will search for a song by calling POST /playlist/addsong/search and pass it the song name or artist name.
    - once the results are listed, Drake will call POST /playlist/addsong which will take the playist name and song id and   add it to his playlist. Drake now has his music in one playlist and can rap along.

# Testing results
<Repeated for each step of the workflow>
1.1  The curl statement called.

 curl -X 'POST' \
  'http://127.0.0.1:8000/musicmain/create_playlist/' \
  -H 'accept: application/json' \
  -H 'access_token: ****' \
  -H 'Content-Type: application/json' \
  -d '{
  "playlist_id": 0,
  "playlist_name": "playlist1",
  "user_id": 1
}'

1.2 The response received.

"Playlist Created"


2.1  The curl statement called.

 curl -X 'POST' \
  'http://127.0.0.1:8000/musicmain/add_song_to_playlist/' \
  -H 'accept: application/json' \
  -H 'access_token: ****' \
  -H 'Content-Type: application/json' \
  -d '{
  "song": {
    "song_id": 2,
    "song_name": "string",
    "artist_name": "string",
    "featured_artist": "string",
    "explicit_rating": 0,
    "length": 0
  },
  "playlist": {
    "playlist_id": 1,
    "playlist_name": "string",
    "user_id": 0
  },
  "user": {
    "user_id": 1,
    "username": "string"
  }
}'



2.2 The response received.

"Song Added to Playlist"

