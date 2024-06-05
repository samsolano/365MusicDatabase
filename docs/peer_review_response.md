
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

<br/> <br/>

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

2. Our add song to playlist endpoint works as intended. It requires song name, artist name, and username.

3. Fix our get ratings endpoint.

Flow 3
1. Upload album is working as intended.

2. Log streams works as intended.

3. Explicit ratings was fixed.

### 2.4 Product Ideas

1. We do not plan on implementing a social aspect as that would require more developement time.

2. We changed our implementation of uploading music to allow for the same song name or album name. This requires for the artist to be different though.

3. We are planning on implementing a search function which should allow for these filters.

<br/> <br/>

## 3. Luca Ornstil Review

The four issues from Luca are as follows:

1. Code Review Comments
2. Schema/API Design Comments
3. Test Resul
4. Product Ideas

### 3.1. Code Review Comments

1. Consistency issues with Render and musicman.py have been resloved.
2. Responses on endpoints now return consistent and useful data.
3. All potential security issues regarding SQL injections have been resolved.
4. Checking the env. variables would be more secure, however we have those set and there is no need to check.
5. Having a log in feature without fixed API_KyEY is something our team decided not to do
6. All Centrel Coast Cauldron code has been removed from the porject code.
7. Our team put a constraint that no album was to have the same name.
8. Our team decided to stick with using a for loops instead of batch inserts.
9. We have now implemented try-except blocks in certain endpoints that would benefit.
10. Our team decided not to implement proper HTTP status codes.
11. We have now addressed the unnecessary imports.
12. Naming consistency issues have now been resoloved.


### 3.2. Schema/API Design Comments

1. It worked fine without this fix
2. We have now added foreign key contraints.
3. We have now changed the nullability of certain columns fo maintain data integrity
4. Our team decided to choose exbool data type instead for our implmentation
5. Our team decided to not create a genre table because it's unnecessary
6. We have now added unique constraints on certain columns.
7. We have now made the dated entries more consistent.
8. We have now prevented null values in certain columns.
9. Since the code is highly dependent on names, changing the consistency of names we decided not to do.
10. We are planning on adding pagination to some of our endpoints
11. We are planning on changing the URLs to our endpoints.
12. We have different explicit content endpoints for different functionality.

### 3.3. Test Results

1. The issues raised in the Test Results have all been addressed and changes have been made to the endpoints to be much more clear and easier to use.

### 3.4. Product Ideas

1. Our team has implemented a similar endpoint to the one recommended and has similar behavior.
2. We have created a playlist viewer that allows the user to view the songs in there playlist, however we decided to not implement the additional analytical data.