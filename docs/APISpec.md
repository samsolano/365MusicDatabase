# API Specification for Music Database

## 1. Requesting Streaming Data

The API calls are made in this sequence when a user
1. `Get Streams`
2. `Get Top 3 Streamed`

### 1.1. Get Streams - `get_streams` (GET)

Gets total number of streams logged

**Response**:
```json
[
    {
        "streamNum": "integer"
    }
]
```

### 1.2. Streams by Artist - (GET)

Gets streams specific to an artist that the user asks for

**Request**:

```json
[
    {
        "artistName": "string"
    }
]
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

## 2. Artist New Song

The API calls are made in this sequence when an artist adds a new song:
1. `Upload Song`

### 2.1. Upload Song - `/new_song/` (POST)

Adds a new song to the music database. Adds a struct Song to the database with song_id being the unique identifier.

**Request**:

```json
{
  "song_id": "string",
  "song_name": "string",
  "artist": "number",
  "album": "string",
  "genre": "string",
  "explicit_rating": "string",
  "label": "string",
  "song_length": "integer",
  "date_added": "string"
}
```

**Response**:

```json
{
    "success": "boolean"
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
    "explicit_rating": "integer",
  }
]
```
## 6. Get Explicit Content.

The API calls are made in this sequence when the User wants to make a playlist:
1. `Get explicit rating` 
2. `List appropiate songs` 

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



