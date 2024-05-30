Possible Concurrency Control Issues:

# 1: Read Skew

    - If a user tries to see the 10 most streamed songs, they will count the total streams of each song, but if they start playing a song in the middle of counting up all the streams, then the 10 most streamed might be in accurate with the actual streams now

    - Solution:
         is to not allow changes while counting up streams, and then as soon as the reading and counting is finished, then allow the
        streams to be added to the streams playlist, so that getting the top 10 is accurate when the user calls for it

# 2: Simultaneous Writes

    - If two users try to upload the same song or album at the same time there could be an issue where there are duplicates or conflicts

    -Solution:
        Use a serializable isolation level to make sure that the insertions are separate, and then add a check to see if the song/album to be uploaded already exists

# 3 Lost Update

    - If two users submit a new explicit rating for a song at the exact same time, they will both take the current rating and then change it based on that initial value which will be the same for both user calls, then one will be overwritten.

    -Solution:
        Use the Repeatable Read isolation level so that another call cant change the average rating until the first call is finished
