# Example workflow

Metro is a big music fan and likes to be on top of every new song from his favorite artists. He wants to be able to add a song into the data base if it hasn't been added. He will start by gathering all the information from the particular song. This includes the song name, artist(s) name, album name, and other important information. Then Metro will send the information to the data base. Lastly, he will get a response on whether the song was successfully added or if it already exists.

# Testing results
<Repeated for each step of the workflow>
1. The curl statement called.
  curl -X 'POST' \
  'http://127.0.0.1:8000/musicmain/upload_music/' \
  -H 'accept: application/json' \
  -H 'access_token: donutHolesApiKey' \
  -H 'Content-Type: application/json' \
  -d '{
  "album_name": "string",
  "song_list": [
    {
      "song_name": "string",
      "artist_name": "string",
      "featured_artist": "string",
      "explicit_rating": 0,
      "length": 0
    }
  ],
  "artist_id": "string",
  "genre": "string",
  "explicit_rating": 0,
  "label": "string",
  "release_date": "string"
}'

2. The response received.
  "Upload Error: Album already exits"
