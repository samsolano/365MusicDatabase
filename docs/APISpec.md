# API Specification for Music Database

## 1. Requesting Streaming Data

User can request three different ways to see streaming data

1. `Get Streams`
2. `Streams Byartist`
3. `Top Streams`

### 1.1. Get Streams - `get_streams` (GET)

Gets total number of streams logged

**Request**:

```json
{
  "user_id": 0,
  "username": "string"
}
```

### 1.2. Streams by Artist - (GET)

Gets streams specific to an artist that the user asks for

**Request**:

```json
{
  "user": {
    "user_id": 0,
    "username": "string"
  },
  "artist": {
    "artist_name": "string"
  }
}
```

**Response**:

```json
[
  {
    "artistName": "string",
    "streamNum": "integer"
  }
]
```

### 1.3. Top Streans - `top_streams` (GET)

Gets the top 10 streamed songs

**Response**:

```json
[
  {
    "Position": "integer",
    "Song": "string",
    "Artist": "string",
    "Streams": "integer"
  }
]
```

## 2. Artist New Song

The API calls are made in this sequence when an artist adds new music:

1. `Create Artist`
2. `Upload New Music`

### 2.1. Create Artist - `/create_artist/` (POST)

Adds a new aritst to the music database. Adds a struct Artist to the database with album_name being the unique identifier

**Request**:

```json
{
  "artist_name": "string"
}
```

**Response**:

```json
{
  "artist_id": "integer"
}
```

### 2.2. Upload New Music - `/upload_music/` (POST)

Adds a new song to the music database. Adds a struct Song to the database with song_id being the unique identifier.

**Request**:

```json
{
  "album_name": "string",
  "artist_name": "string",
  "song_list": [
    {
      "song_name": "string",
      "artist_name": "string",
      "featured_artist": "string",
      "explicit_rating": 0,
      "length": 0
    }
  ],
  "genre": "string",
  "explicit_rating": 0,
  "label": "string",
  "release_date": "string"
}
```

**Response**:

```json
{
  "success": "string"
}
```

## 3. Make a playlist.

The API calls are made in this sequence when the User wants to make a playlist:

1. `Give Playlist Name`
2. `List Song Suggestions`
3. `Search For Songs`
4. `Add Song to Playlist`

### 3.1. Give Playlist Name - `/playlist/newplaylist` (POST)

The user creates a playlist and gives it a name.

**Request**:

```json
[
  {
    "playlist_name": "string"
  }
]
```

**Response**:

```json
{
  "success": "string"
}
```

### 3.2. List Song Suggestions - `/playlist/make` (POST)

Lists some songs the user can pick from to start their playlist.

**Response**:

```json
[
  {
    "top_songs": "string"
  }
]
```

### 3.3. Search For Songs - `/playlist/addsong/search` (POST)

Allows the user to search for a song by name or by artist to add to their playlist.

**Request**:

```json
[
  {
    "artist_name": "string",
    "song_name": "string"
  }
]
```

**Response**:

```json
{
  "search_results": "string",
  "song_name": "string",
  "song_id": "integer"
}
```

### 3.4. Add Song to Playlist - `/playlist/addsong` (POST)

Allows the User to add a song to a playlist

**Request**:

```json
[
  {
    "playlist_name": "string",
    "song_name": "string",
    "song_id": "integer"
  }
]
```

**Response**:

```json
{
  "success": "string"
}
```

## 4. Like Songs and Add to 'Liked' Playlist

The API calls are made in this sequence when the User likes a song:

1. `Get Song ID`
2. `Add to Liked Songs`

### 2.1. Get Song ID - `/songs/id` (POST)

Gets the song ID for the song that was liked by the User.

**Request**:

```json
[
  {
    "song_name": "string",
    "artist_name": "string"
  }
]
```

**Response**:

```json
[
  {
    "song_id": "integer"
  }
]
```

### 2.2. Add to Liked Songs - `/playlist/likedsongs` (POST)

Add the song the User liked to the 'Liked Songs' playlist.

**Request**:

```json
[
  {
    "song_id": "integer"
  }
]
```

**Response**:

```json
{
  "success": "string"
}
```

## 5. Get Explicit Content.

The API calls are made in this sequence when the User wants to make a playlist:

1. `Submit explicit rating`

### 5.1. Submit Explicit Content Rating - `/song/input_explicit` (POST)

Submit an explicit content rating.

**Request**:

```json
[
  {
    "song_id": "string",
    "explicit_rating": "integer"
  }
]
```

## 6. Get Explicit Content.

The API calls are made in this sequence when the User wants to make a playlist:

1. `Get explicit rating`
2. `List appropiate songs`
3. `Submit Explicit`

### 6.1. Get explicit - `/songs/get_explicit` (POST)

Returns a the explicit rating of a song.

**Return**:

```json
[
  {
    "explicit": "floating"
  }
]
```

### 6.2. Get non explicit songs - `/songs/non_explicit_list` (POST)

Returns a the explicit rating of a song.
**Request**:

```json
[
  {
    "rating": "floating"
  }
]
```

**Response**:

```json
[
  {
    "song_id": "integer",
    "explicit": "floating"
  }
]
```

### 6.3. Submit Explicit Rating - `/songs/submit_rating` (POST)

Returns if successful.
**Request**:

```json
[
  {
    "song": "string",
    "rating": "int"
  }
]
```

**Response**:

```json
{
  "success": "boolean"
}
```
