# Example Flows

# 1:
    Kendrick has been looking for a place to be able to log all of his song streaming info in one easy place. So he came to us to start logging his streams. 
    He first uses GET /streams and then he is gonna see all of the songs he has streamed, the number of times, the artist, and the genre of the songs.
    He then is curious about how many times he has streamed Stevie's music so he calls GET /streams by artist. He first updates with all of the songs
    that he has been listening to so that the database is up to date. Then he calls check streams to see that it has all been updated. Then he calls the get streams by artist and passes in Stevie's name and then the amount of songs streamed of Stevie's music are returned as an int.
s