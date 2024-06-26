User Stories:
<!-- Sam -->>
1: As a DJ I want to track my streams so I can remember which songs to keep playing.

    Exception: the number of streams overflows the integer limit
    Solution: We will make sure to check the integers to not overflow and maybe restore streams in a different row with the same song

2: As the owner of a bar I want to put on popular playlists and track which artists are played the most so that I can start to play the most popular artists

    Exception: The same song repeating doesn't increase total number of streams for that song individually
    Solution: Make sure that we keep an int for tracking total plays of a single song

3: As a musician I want to be able to track my most played genres so that I can track what songs/artists influence my music

    Exception: The genres might not line up exactly with how the artist sees fit
    Solution: We can group based on multiple genres and perhaps by artistic movement/scene too

<!-- Carlos -->

4: As a music enthusiast, I want to search for artists by name or genre, so that I can discover new music and playlists.

    Exception: When a user enters a search term that does not match any artists, songs, or genres in the database, the system will give an error message.
    Solution: A possible solution to this problem would be an implementation of an auto-suggest feature that lists the possible inputs from a table.

5: As a Spotify user, I want to be able to like songs and have them automatically added to a 'Liked Songs' playlist, so that I can easily find my favorite tracks later.

    Exception: If a user tries to create a new playlist with a name that already exists in their account, the system should prompt the user to choose a different name.
    Solution: A solution to this would be to create a user id and allow for multiple playlists of the same name.

6: As a playlist creator, I want to create and name my own playlists, add songs to them, and edit them at any time, so that I can share them with friends.
Exception: When a user shares a playlist, there might be problems regarding who can access or edit the playlist.
Solution: To fix this issue, our implementation should ensure that only the user with the primary key is able to edit but anyone else can only view.

<!-- Ryan  -->

7: As a music streamer, I want to be able to see my most played songs, so that I can know what I'm playing the most.

    Exception: Inaccurate tracking of play counts
    Solution: If a user notices that their top song stream are showing inaccurate play counts, the user can submit a report that flags the issue.

8: As a music streamer, I want to be able to see my friends most played songs, so I can compare them to my most listened songs.

    Exception: Friends have no streams
    Solution: If a user checks a friend who has no most played songs since they don't stream, an error could occur with how the data is shown, the solution would be to let the user know there are none and handle it correctly.

9: As a music streamer, I want to see the last played songs from my friends, so that I can see what they've been listening to recently.

    Exception: Incorrect last song
    Solution: When a user checks their friends' last played song, it could not be updated correctly. A solution is to make sure when a song is streamed it gets corretly updated in the database.

<!-- Kin -->

10:As a music designer, I want to access a diverse library of instrumental samples from songs categorized by genre and mood, so that I can quickly find the right elements to create unique compositions for my projects.

    Exception: Some instruments may not be recognized or indistinguishable
    Solution: A song could have no description of instruments. A solution could be a user could submit a list of instruments that are distinguishable and gets added to the database.  

11:As a music historian, I want to explore curated collections of music from specific eras or movements, so that I can study the evolution of musical styles over time.

    Exception: Song has no record of release date.
    Solution: We can match the song to other songs that have a similar sound signature, instruments, genre, lyrics, and date the unknown song with the other songs, with a disclosure that the date matched unknown song is an educated guess. 

12:As a parent, I want to set up parental controls to restrict explicit content, so that I can ensure my children are listening to age-appropriate music.

    Exception: No record of the lyrics or inaccurate lyrics with the song.
    Solution: Each song would have an explicit integer, one for explicit, 0 for non-explicit music. If there is no official lyric release from the artist themselves, then a user could a 1 for explicit and 0 for not saying the song is inappropriate and a generated explicit rating could be associated with the song, a number between 1 and 0, 1 being very explicit, and 0 being not explicit at all. 
