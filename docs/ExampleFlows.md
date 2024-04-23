# Example Flows

# 1:
    Kendrick has been looking for a place to be able to log all of his song streaming info in one easy place. So he came to us to start logging his streams. 
    He first uses GET /streams and then he is gonna see all of the songs he has streamed, the number of times, the artist, and the genre of the songs.
    He then is curious about how many times he has streamed Stevie's music so he calls GET /streams by artist. He first updates with all of the songs
    that he has been listening to so that the database is up to date. Then he calls check streams to see that it has all been updated. Then he calls the get streams by artist and passes in Stevie's name and then the amount of songs streamed of Stevie's music are returned as an int.

# 2:
    Drake is big fan of Rap music. He wants to make a compilation of the greatest diss tracks ever made. To do so, he needs to make a playlist. Drake needs to:
    - start by calling POST /playlist/newplaylist and give his playlist a name. He chooses to name it Rap Beef.
    - then Drake will search for a song by calling POST /playlist/addsong/search and pass it the song name or artist name.
    - once the results are listed, Drake will call POST /playlist/addsong which will take the playist name and song id and   add it to his playlist.

    Drake now has his music in one playlist and can rap along.

# 3:
    Jermaine wants his kids to be able to listen to kid friendly music. To do so, Jermaine needs to:
    - 