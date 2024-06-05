# Peer Reviews Responses

## 1. Noah Giboney

1. Schema Comments
2. Code Review Comments
3. Test Results
4. Product Ideas

### 1.1. Schema Comments

1. We added foreign keys already to our tables
2. Fixed all Class variables to have same snake_case convention
3. This one doesn't make sense
4. We have unique constraints in our user table, the user_id
5. We have a created_at in every table we have
6. We implemented it that way because we plan on having user submissions for explicit ratings from 1-1a
7. We fixed it, the only possible null column was the featured artists but now its just empty
8. Ok fixed that, got rid of the two id columns that had strin
9. There is now only a single endpoint for user submitted ratings
10. Added an index to make stuff faster
11. Added more catch blocks to handle errors
12. Not necessary for most of our endpoints

### 1.2 Code Review Comments

1. I'm not sure how we would authorize each endpoint, We have the API Key to check if people are allowed to use our endpoints
2.  Will get rid of the docs page that still had Central Coast Cauldrons
3. Will fix the indentation
4. Redeployed sorry about that, theyre all current now and working
5. Probably wise long term but for our project won't be necessary
6. We will make sure to make all consistent
7. Got rid of all formatting to ensure no sql injections
8. We added more catches to check for errors
9. We print strings in order to make it obvious that it was successful
10. 
11. We have the sql check it now
12. Will address that and check for NULL values ----------------------



### 1.3. Test Results

Unfortunately our Render was down when these tests were run, so Noah was not able to run our code, but we have redeployed it to Render and have made sure our endpoints are working

But for his test flows we can still address them.

1. This is possible and would work with our endpoints create playlist and add songs to playlist

2. This works fine, adding songs to the library with the info is possible

3. It would be done differently but it would be different, you would call our get_clean_songs and then add them to a playlist for her kids, and if she disagreed with a songs rating she could submit a user explicit rating



### 1.4 Product Ideas

1. This is a good idea, I will definitely add a delete song from playlist endpoint-----------
2. I also think this is a good idea, but sharing songs and playlists is probably out of the scope of this project. Also not sure how sharing songs and playlists would work





## 2. Jesus Avalos Review
### 2.1. Code Review

1. Did not implement account creating for api key as security is not a concern.

2. Fixed api route not being displayed.

3. We require api key to use our site.

4. Removed Cenctral Coast Cauldrons references.

5. Albums now require artist name as well.

6. Create playlist now uses playlist name and username. Log stream uses song_id.

7. We now only use username and not user_id.

8. Changed our code, it now uses a query.

9. Need to implement exception handling for user not existing.

10. No longer use artist_id and use artist name instead.

11. We are currently working on a search/view songs endpoint.

12. We changed the return messages from just "OK".


### 2.2. Schema/API Design

1. We changed our streams table and has a foreign key now.

2. Not needed, int works the same in our implementation.

3. Added a foreign key to playlists. No longer set to NULL.

4. Users table no longer allows Nullable usernames.

5. Songs table has artist_id as foreign key now. 

6. Changed songid to song_id in explicit_submissions table.

7. Changed artist table to not allow NULL names

8. Removed nullable from album table. Added foreign key to artist_id.

9. Our code only allows for one album name. 

10. We do plan to split our routes by topic. Coming soon.

11. No particular reason for the naming format. It just be like that.

12. We do plan to change the name of the routes for readability. 


### 2.3 Test Results

Flow 1
1. Our add_user function no longer require user_id, only username.

2. In our log_streams function, we now require song_name, artist_name, and username. We also added catches if any field doesn't exist.

3. Changed our get_streams funtion to only require a username.1a

Flow 2
1. Create playlist now requires playlist name and username. Also prints a message.

2. 

3.

### 2.4 Product Ideas




## 3. Luca Ornstil Review

The four issues from Luca are as follows:

1. `Code Review Comments`
2. `Schema/API Design Comments`
3. `Test Results`
4. `Product Ideas`

### 3.1. Code Review Comments

1. Consistency issues with Render and musicman.py have been resloved.
2. Responses on endpoints now return consistent and useful data.
3. All potential security issues regarding SQL injections have been resolved.
4. Checking the env. variables would be more secure, however we have those set and there is no need to check.
5. Having a log in feature without fixed API_KyEY is something our team decided not to do
6. All Centrel Coast Cauldron code has been removed from the porject code.
7. Our team put a constraint that no album was to have the same name.
8. Our team decided to stick with using a for loops instead of batch inserts.
9. 


### 3.2. Song Reccomendation - `reccomend_song` (POST)

Lists a song in a genre the user might be interested in for a playlist

**Response**:

```json
[
  {
    "song_suggestion": "string"
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
  "success": "boole yee
}
```
