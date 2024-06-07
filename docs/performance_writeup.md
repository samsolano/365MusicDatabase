# Performance Writeup

1. Fake Data Modeling
2. Performance Results of Endpoints
3. Performance Tuning

### 1. Fake Data Modeling

    -Explanation:
        We have a total of ___ rows in our tables, which is split up as:
            - albums: 1682
            - artist: 181
            - explicit_submissions: 4
            - song: 26741
            - song_playlist:5374725
            - streams: 5774216
            - user_playlist: 250002
            - users:  40,013

        We think that realisitically there would be far more songs, which would add more artists, and albums. But we do think it makes sense that users would make lots of playlists and with lots of different songs in those playlists, and that users would have many streams from all the times they play their playlists and favorite songs.

    - Python Code:
        Code listed at bottom

### 2. Performance Results of Endpoints

    Three slowest Endpoints:
        1: Recommend New Songs: 932 ms
        2: Top Streams: 843 ms
        3: Remove Song From Playlist: 815 ms

    -Add User:
        - Execution Time(ms): 464

    -Create Artist:
        - Execution Time(ms): 391

    -Upload New Music:
        - Execution Time(ms): 521

    -Search For Song:
        - Execution Time(ms): 629

    -Search For Artist:
        - Execution Time(ms): 441

    - Search For Album:
        - Execution Time(ms): 590

    -Artist Albums:
        - Execution Time(ms): 371

    -Album Songs:
        - Execution Time(ms): 748

    -Song Info:
        - Execution Time(ms): 396

    -Album Info:
        - Execution Time(ms): 571

    -Log Streams:
        - Execution Time(ms): 688

    -Get Streams:
        - Execution Time(ms): 465

    -Streams By Artist:
        - Execution Time(ms): 620

    -Create Playlist:
        - Execution Time(ms): 411

    -Add Songs To Playlist:
        - Execution Time(ms): 501

    -View Playlist
        - Execution Time(ms): 522

    -Add Rating To Song
        - Execution Time(ms): 573

    -Get Clean Songs
        - Execution Time(ms): 457

    -Recommend Song
        - Execution Time(ms): 732

    -Top Streams
        - Execution Time(ms): 843

    -Recommend New Songs
        - Execution Time(ms): 932

    -Remove Song From Playlist
        - Execution Time(ms): 815

### 3. Performance Tuning

    Three slowest Endpoints:

        1: Recommend New Songs:   //index on song_playlist
            - Old Time: 932 ms
            - New Time:

        2: Top Streams:           //index on streams
            - Old Time: 843 ms
            - New Time:

        3: Remove Song From Playlist:    //index on song_playlist
            - Old Time: 815 ms
            - New Time:

    Fixes:
        1:
            -Command:
            -Explanation:

        2:
            -Command:
            -Explanation:

        3:
            -Command:
            -Explanation:

# Python Code:

## shiftid.py:

    import pandas as pd

    # Load the CSV file
    file_path = 'playlist_songs.csv'
    playlists_df = pd.read_csv(file_path)

    # Function to modify playlist IDs
    def modify_playlist_id(playlist_id):
        new_id = (playlist_id + 5) % 35005
        if playlist_id + 5 > 35005:
            return 25006 + new_id
        return new_id

    # Apply the function to the 'playlist_id' column
    playlists_df['playlist_id'] = playlists_df['playlist_id'].apply(modify_playlist_id)

    # Save the modified DataFrame back to CSV
    playlists_df.to_csv('modified_playlists.csv', index=False)

    print("Playlist IDs have been modified and saved to 'modified_playlists.csv'.")

## usergen.py:

    import csv

    # Define the file name
    output_file = 'usernames.csv'

    # Open the file for writing
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['username'])
        # Write the usernames
        for i in range(1, 40001):
            writer.writerow([f'user{i}'])

    print(f'{output_file} has been created successfully.')

## userplaylistgen.py:

    import csv

    # Define the file name
    output_file = 'playlists.csv'

    # Open the file for writing
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['playlist_name', 'user_id'])
        # Write the playlist data
        for user_index, user_id in enumerate(range(10013, 40011), start=10013):
            for playlist_num in range(1, 6):
                playlist_name = f'u{user_index}p{playlist_num}'
                writer.writerow([playlist_name, user_id])

    print(f'{output_file} has been created successfully.')

## discography_scrape.py:

    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import json

    # Initialize Spotipy with user credentials
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    print("went through credentials")
    # List of artists
    artists = [""]  # Replace with your list of artists

    # Function to get the artist's discography
    def get_artist_id(name):
        result = sp.search(q='artist:' + name, type='artist')
        items = result['artists']['items']
        if items:
            return items[0]['id']
        else:
            return None

    def get_album_tracks(album_id):
        tracks_info = []
        results = sp.album_tracks(album_id)
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])

        for track in tracks:
            featured_artists = [artist['name'] for artist in track['artists'][1:]]
            track_info = {
                "song_name": track['name'],
                "artist_name": track['artists'][0]['name'],
                "featured_artist": featured_artists[0] if featured_artists else "",
                "explicit_rating": track['explicit'],
                "length": track['duration_ms'] // 1000  # Convert duration to seconds
            }
            tracks_info.append(track_info)
        return tracks_info

    def get_discography(artist_name, artist_id):
        albums_info = []
        results = sp.artist_albums(artist_id, album_type='album')
        albums = results['items']
        while results['next']:
            results = sp.next(results)
            albums.extend(results['items'])

        for album in albums:
            album_details = sp.album(album['id'])
            genres = album_details['genres']
            genre = ", ".join(genres) if genres else "genre"
            album_info = {
                "album_name": album['name'],
                "artist_name": artist_name,
                "song_list": get_album_tracks(album['id']),
                "genre": genre,
                "explicit_rating": int(any(track['explicit'] for track in album_details['tracks']['items'])),
                "label": album_details['label'],
                "release_date": album['release_date']
            }
            albums_info.append(album_info)
        return albums_info

    all_discographies = []

    for artist in artists:
        artist_id = get_artist_id(artist)
        if artist_id:
            albums_info = get_discography(artist, artist_id)
            all_discographies.extend(albums_info)

    # Write the discography to a JSON file
    with open('discography.json', 'w', encoding='utf-8') as f:
        json.dump(all_discographies, f, ensure_ascii=False, indent=4)

    print("Discography data has been written to discography.json")
