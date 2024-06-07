# Performance Writeup

1. Fake Data Modeling
2. Performance Results of Endpoints
3. Performance Tuning

### 1. Fake Data Modeling

    -Explanation:
        We have a total of 11,467,564 rows in our tables, which is split up as:
            - albums: 1,682
            - artist: 181
            - explicit_submissions: 4
            - song: 26,741
            - song_playlist: 5,374,725
            - streams: 5,774,216
            - user_playlist: 250,002
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

        1: Recommend New Songs:
            - Old Time After Explain Analyze: 7628 ms
            - New Time: 1835 ms

**Before**

```json
[
  {
    "QUERY PLAN": "Limit  (cost=308951.97..308952.04 rows=5 width=60) (actual time=7618.344..7626.272 rows=3 loops=1)"
  },
  {
    "QUERY PLAN": "  CTE playlist_6_songs"
  },
  {
    "QUERY PLAN": "    ->  Gather  (cost=4834.56..84277.61 rows=21 width=8) (actual time=2724.031..2732.016 rows=10 loops=1)"
  },
  {
    "QUERY PLAN": "          Workers Planned: 1"
  },
  {
    "QUERY PLAN": "          Workers Launched: 1"
  },
  {
    "QUERY PLAN": "          ->  Nested Loop  (cost=3834.56..83275.51 rows=12 width=8) (actual time=2283.070..2720.395 rows=5 loops=2)"
  },
  {
    "QUERY PLAN": "                ->  Parallel Hash Join  (cost=3834.26..83270.41 rows=12 width=16) (actual time=2282.911..2720.232 rows=5 loops=2)"
  },
  {
    "QUERY PLAN": "                      Hash Cond: (song_playlist.playlist_id = up_1.playlist_id)"
  },
  {
    "QUERY PLAN": "                      ->  Parallel Seq Scan on song_playlist  (cost=0.00..71136.85 rows=3161585 width=16) (actual time=0.452..2485.379 rows=2687362 loops=2)"
  },
  {
    "QUERY PLAN": "                      ->  Parallel Hash  (cost=3834.24..3834.24 rows=1 width=16) (actual time=13.272..13.273 rows=0 loops=2)"
  },
  {
    "QUERY PLAN": "                            Buckets: 1024  Batches: 1  Memory Usage: 40kB"
  },
  {
    "QUERY PLAN": "                            ->  Parallel Seq Scan on user_playlist up_1  (cost=0.00..3834.24 rows=1 width=16) (actual time=5.344..13.237 rows=0 loops=2)"
  },
  {
    "QUERY PLAN": "                                  Filter: (playlist_name = 'u1p1'::text)"
  },
  {
    "QUERY PLAN": "                                  Rows Removed by Filter: 125000"
  },
  {
    "QUERY PLAN": "                ->  Memoize  (cost=0.30..2.52 rows=1 width=8) (actual time=0.032..0.032 rows=1 loops=10)"
  },
  {
    "QUERY PLAN": "                      Cache Key: up_1.user_id"
  },
  {
    "QUERY PLAN": "                      Cache Mode: logical"
  },
  {
    "QUERY PLAN": "                      Worker 0:  Hits: 9  Misses: 1  Evictions: 0  Overflows: 0  Memory Usage: 1kB"
  },
  {
    "QUERY PLAN": "                      ->  Index Only Scan using users_pkey on users u_1  (cost=0.29..2.51 rows=1 width=8) (actual time=0.076..0.076 rows=1 loops=1)"
  },
  {
    "QUERY PLAN": "                            Index Cond: (user_id = up_1.user_id)"
  },
  {
    "QUERY PLAN": "                            Heap Fetches: 1"
  },
  {
    "QUERY PLAN": "  ->  Unique  (cost=224674.36..224747.47 rows=5849 width=60) (actual time=7618.343..7618.358 rows=3 loops=1)"
  },
  {
    "QUERY PLAN": "        ->  Sort  (cost=224674.36..224688.98 rows=5849 width=60) (actual time=7618.341..7618.351 rows=3 loops=1)"
  },
  {
    "QUERY PLAN": "              Sort Key: sp.song_id, s.song_name, al.album_name, art.artist_name"
  },
  {
    "QUERY PLAN": "              Sort Method: quicksort  Memory: 25kB"
  },
  {
    "QUERY PLAN": "              ->  Hash Join  (cost=110451.54..224308.39 rows=5849 width=60) (actual time=7237.695..7618.317 rows=3 loops=1)"
  },
  {
    "QUERY PLAN": "                    Hash Cond: (sp.song_id = s.song_id)"
  },
  {
    "QUERY PLAN": "                    ->  Hash Join  (cost=109367.64..223126.76 rows=10463 width=8) (actual time=7213.909..7594.521 rows=10 loops=1)"
  },
  {
    "QUERY PLAN": "                          Hash Cond: (sp.playlist_id = sp_1.playlist_id)"
  },
  {
    "QUERY PLAN": "                          ->  Seq Scan on song_playlist sp  (cost=0.47..106705.16 rows=2687348 width=16) (actual time=2725.627..4275.969 rows=5374317 loops=1)"
  },
  {
    "QUERY PLAN": "                                Filter: (NOT (hashed SubPlan 2))"
  },
  {
    "QUERY PLAN": "                                Rows Removed by Filter: 408"
  },
  {
    "QUERY PLAN": "                                SubPlan 2"
  },
  {
    "QUERY PLAN": "                                  ->  CTE Scan on playlist_6_songs playlist_6_songs_1  (cost=0.00..0.42 rows=21 width=8) (actual time=2724.033..2724.110 rows=10 loops=1)"
  },
  {
    "QUERY PLAN": "                          ->  Hash  (cost=109357.33..109357.33 rows=787 width=8) (actual time=2853.468..2853.473 rows=1 loops=1)"
  },
  {
    "QUERY PLAN": "                                Buckets: 1024  Batches: 1  Memory Usage: 9kB"
  },
  {
    "QUERY PLAN": "                                ->  GroupAggregate  (cost=109302.26..109349.46 rows=787 width=8) (actual time=2853.129..2853.470 rows=1 loops=1)"
  },
  {
    "QUERY PLAN": "                                      Group Key: sp_1.playlist_id"
  },
  {
    "QUERY PLAN": "                                      Filter: (count(DISTINCT sp_1.song_id) >= 3)"
  },
  {
    "QUERY PLAN": "                                      Rows Removed by Filter: 388"
  },
  {
    "QUERY PLAN": "                                      ->  Sort  (cost=109302.26..109308.16 rows=2360 width=16) (actual time=2853.073..2853.102 rows=398 loops=1)"
  },
  {
    "QUERY PLAN": "                                            Sort Key: sp_1.playlist_id"
  },
  {
    "QUERY PLAN": "                                            Sort Method: quicksort  Memory: 46kB"
  },
  {
    "QUERY PLAN": "                                            ->  Nested Loop  (cost=1.39..109170.04 rows=2360 width=16) (actual time=32.629..2852.656 rows=398 loops=1)"
  },
  {
    "QUERY PLAN": "                                                  ->  Nested Loop  (cost=1.10..108443.16 rows=2360 width=24) (actual time=32.616..2850.877 rows=398 loops=1)"
  },
  {
    "QUERY PLAN": "                                                        ->  Hash Semi Join  (cost=0.68..107403.46 rows=2360 width=16) (actual time=32.577..2846.503 rows=408 loops=1)"
  },
  {
    "QUERY PLAN": "                                                              Hash Cond: (sp_1.song_id = playlist_6_songs.song_id)"
  },
  {
    "QUERY PLAN": "                                                              ->  Seq Scan on song_playlist sp_1  (cost=0.00..93267.95 rows=5374695 width=16) (actual time=0.008..2384.275 rows=5374725 loops=1)"
  },
  {
    "QUERY PLAN": "                                                              ->  Hash  (cost=0.42..0.42 rows=21 width=8) (actual time=0.012..0.013 rows=10 loops=1)"
  },
  {
    "QUERY PLAN": "                                                                    Buckets: 1024  Batches: 1  Memory Usage: 9kB"
  },
  {
    "QUERY PLAN": "                                                                    ->  CTE Scan on playlist_6_songs  (cost=0.00..0.42 rows=21 width=8) (actual time=0.001..0.002 rows=10 loops=1)"
  },
  {
    "QUERY PLAN": "                                                        ->  Index Scan using user_playlist_pkey on user_playlist up  (cost=0.42..0.44 rows=1 width=16) (actual time=0.009..0.009 rows=1 loops=408)"
  },
  {
    "QUERY PLAN": "                                                              Index Cond: (playlist_id = sp_1.playlist_id)"
  },
  {
    "QUERY PLAN": "                                                              Filter: (playlist_name <> 'u1p1'::text)"
  },
  {
    "QUERY PLAN": "                                                              Rows Removed by Filter: 0"
  },
  {
    "QUERY PLAN": "                                                  ->  Index Only Scan using users_pkey on users u  (cost=0.29..0.31 rows=1 width=8) (actual time=0.003..0.003 rows=1 loops=398)"
  },
  {
    "QUERY PLAN": "                                                        Index Cond: (user_id = up.user_id)"
  },
  {
    "QUERY PLAN": "                                                        Heap Fetches: 18"
  },
  {
    "QUERY PLAN": "                    ->  Hash  (cost=749.64..749.64 rows=26741 width=56) (actual time=23.700..23.703 rows=26741 loops=1)"
  },
  {
    "QUERY PLAN": "                          Buckets: 32768  Batches: 1  Memory Usage: 2664kB"
  },
  {
    "QUERY PLAN": "                          ->  Hash Join  (cost=65.02..749.64 rows=26741 width=56) (actual time=0.667..17.491 rows=26741 loops=1)"
  },
  {
    "QUERY PLAN": "                                Hash Cond: (s.artist_id = art.id)"
  },
  {
    "QUERY PLAN": "                                ->  Hash Join  (cost=58.95..671.73 rows=26741 width=49) (actual time=0.593..12.026 rows=26741 loops=1)"
  },
  {
    "QUERY PLAN": "                                      Hash Cond: (s.album_id = al.id)"
  },
  {
    "QUERY PLAN": "                                      ->  Seq Scan on song s  (cost=0.00..542.41 rows=26741 width=32) (actual time=0.006..5.711 rows=26741 loops=1)"
  },
  {
    "QUERY PLAN": "                                      ->  Hash  (cost=38.42..38.42 rows=1642 width=25) (actual time=0.576..0.577 rows=1682 loops=1)"
  },
  {
    "QUERY PLAN": "                                            Buckets: 2048  Batches: 1  Memory Usage: 113kB"
  },
  {
    "QUERY PLAN": "                                            ->  Seq Scan on album al  (cost=0.00..38.42 rows=1642 width=25) (actual time=0.003..0.255 rows=1682 loops=1)"
  },
  {
    "QUERY PLAN": "                                ->  Hash  (cost=3.81..3.81 rows=181 width=15) (actual time=0.065..0.065 rows=181 loops=1)"
  },
  {
    "QUERY PLAN": "                                      Buckets: 1024  Batches: 1  Memory Usage: 17kB"
  },
  {
    "QUERY PLAN": "                                      ->  Seq Scan on artist art  (cost=0.00..3.81 rows=181 width=15) (actual time=0.010..0.032 rows=181 loops=1)"
  },
  {
    "QUERY PLAN": "Planning Time: 2.362 ms"
  },
  {
    "QUERY PLAN": "Execution Time: 7628.325 ms"
  }
]
```

**After**

```json
[
  {
    "QUERY PLAN": "Limit  (cost=118084.87..118084.93 rows=5 width=60) (actual time=1835.280..1835.293 rows=3 loops=1)"
  },
  {
    "QUERY PLAN": "  CTE playlist_6_songs"
  },
  {
    "QUERY PLAN": "    ->  Nested Loop  (cost=1.14..3440.03 rows=21 width=8) (actual time=0.044..9.850 rows=10 loops=1)"
  },
  {
    "QUERY PLAN": "          ->  Nested Loop  (cost=0.71..3435.55 rows=1 width=8) (actual time=0.031..9.831 rows=1 loops=1)"
  },
  {
    "QUERY PLAN": "                ->  Index Only Scan using idx_user_playlist_user_id_playlist_id_playlist_name on user_playlist up_1  (cost=0.42..3433.05 rows=1 width=16) (actual time=0.018..9.818 rows=1 loops=1)"
  },
  {
    "QUERY PLAN": "                      Index Cond: (playlist_name = 'u1p1'::text)"
  },
  {
    "QUERY PLAN": "                      Heap Fetches: 1"
  },
  {
    "QUERY PLAN": "                ->  Index Only Scan using idx_users_user_id on users u_1  (cost=0.29..2.51 rows=1 width=8) (actual time=0.011..0.011 rows=1 loops=1)"
  },
  {
    "QUERY PLAN": "                      Index Cond: (user_id = up_1.user_id)"
  },
  {
    "QUERY PLAN": "                      Heap Fetches: 1"
  },
  {
    "QUERY PLAN": "          ->  Index Only Scan using idx_song_playlist_playlist_id_song_id on song_playlist  (cost=0.43..4.21 rows=27 width=16) (actual time=0.012..0.016 rows=10 loops=1)"
  },
  {
    "QUERY PLAN": "                Index Cond: (playlist_id = up_1.playlist_id)"
  },
  {
    "QUERY PLAN": "                Heap Fetches: 10"
  },
  {
    "QUERY PLAN": "  ->  Unique  (cost=114644.84..114717.95 rows=5849 width=60) (actual time=1835.279..1835.289 rows=3 loops=1)"
  },
  {
    "QUERY PLAN": "        ->  Sort  (cost=114644.84..114659.46 rows=5849 width=60) (actual time=1835.278..1835.283 rows=3 loops=1)"
  },
  {
    "QUERY PLAN": "              Sort Key: sp.song_id, s.song_name, al.album_name, art.artist_name"
  },
  {
    "QUERY PLAN": "              Sort Method: quicksort  Memory: 25kB"
  },
  {
    "QUERY PLAN": "              ->  Nested Loop  (cost=110239.31..114278.86 rows=5849 width=60) (actual time=1834.873..1835.248 rows=3 loops=1)"
  },
  {
    "QUERY PLAN": "                    ->  Hash Join  (cost=110239.17..113328.00 rows=5849 width=53) (actual time=1834.863..1835.233 rows=3 loops=1)"
  },
  {
    "QUERY PLAN": "                          Hash Cond: (s.album_id = al.id)"
  },
  {
    "QUERY PLAN": "                          ->  Hash Join  (cost=110180.22..113253.65 rows=5849 width=36) (actual time=1834.294..1834.662 rows=3 loops=1)"
  },
  {
    "QUERY PLAN": "                                Hash Cond: (sp.song_id = s.song_id)"
  },
  {
    "QUERY PLAN": "                                ->  Nested Loop  (cost=109303.55..112349.51 rows=10463 width=8) (actual time=1823.751..1824.121 rows=10 loops=1)"
  },
  {
    "QUERY PLAN": "                                      ->  GroupAggregate  (cost=109302.64..109349.84 rows=787 width=8) (actual time=1823.713..1824.075 rows=1 loops=1)"
  },
  {
    "QUERY PLAN": "                                            Group Key: sp_1.playlist_id"
  },
  {
    "QUERY PLAN": "                                            Filter: (count(DISTINCT sp_1.song_id) >= 3)"
  },
  {
    "QUERY PLAN": "                                            Rows Removed by Filter: 388"
  },
  {
    "QUERY PLAN": "                                            ->  Sort  (cost=109302.64..109308.54 rows=2360 width=16) (actual time=1823.686..1823.717 rows=398 loops=1)"
  },
  {
    "QUERY PLAN": "                                                  Sort Key: sp_1.playlist_id"
  },
  {
    "QUERY PLAN": "                                                  Sort Method: quicksort  Memory: 46kB"
  },
  {
    "QUERY PLAN": "                                                  ->  Nested Loop  (cost=1.39..109170.43 rows=2360 width=16) (actual time=43.717..1823.307 rows=398 loops=1)"
  },
  {
    "QUERY PLAN": "                                                        ->  Nested Loop  (cost=1.10..108443.54 rows=2360 width=24) (actual time=43.702..1821.152 rows=398 loops=1)"
  },
  {
    "QUERY PLAN": "                                                              ->  Hash Semi Join  (cost=0.68..107403.84 rows=2360 width=16) (actual time=43.674..1814.891 rows=408 loops=1)"
  },
  {
    "QUERY PLAN": "                                                                    Hash Cond: (sp_1.song_id = playlist_6_songs.song_id)"
  },
  {
    "QUERY PLAN": "                                                                    ->  Seq Scan on song_playlist sp_1  (cost=0.00..93268.25 rows=5374725 width=16) (actual time=0.306..1345.295 rows=5374725 loops=1)"
  },
  {
    "QUERY PLAN": "                                                                    ->  Hash  (cost=0.42..0.42 rows=21 width=8) (actual time=9.861..9.861 rows=10 loops=1)"
  },
  {
    "QUERY PLAN": "                                                                          Buckets: 1024  Batches: 1  Memory Usage: 9kB"
  },
  {
    "QUERY PLAN": "                                                                          ->  CTE Scan on playlist_6_songs  (cost=0.00..0.42 rows=21 width=8) (actual time=0.046..9.855 rows=10 loops=1)"
  },
  {
    "QUERY PLAN": "                                                              ->  Index Scan using user_playlist_pkey on user_playlist up  (cost=0.42..0.44 rows=1 width=16) (actual time=0.013..0.013 rows=1 loops=408)"
  },
  {
    "QUERY PLAN": "                                                                    Index Cond: (playlist_id = sp_1.playlist_id)"
  },
  {
    "QUERY PLAN": "                                                                    Filter: (playlist_name <> 'u1p1'::text)"
  },
  {
    "QUERY PLAN": "                                                                    Rows Removed by Filter: 0"
  },
  {
    "QUERY PLAN": "                                                        ->  Index Only Scan using idx_users_user_id on users u  (cost=0.29..0.31 rows=1 width=8) (actual time=0.004..0.004 rows=1 loops=398)"
  },
  {
    "QUERY PLAN": "                                                              Index Cond: (user_id = up.user_id)"
  },
  {
    "QUERY PLAN": "                                                              Heap Fetches: 18"
  },
  {
    "QUERY PLAN": "                                      ->  Index Only Scan using idx_song_playlist_playlist_id_song_id on song_playlist sp  (cost=0.91..3.67 rows=13 width=16) (actual time=0.035..0.041 rows=10 loops=1)"
  },
  {
    "QUERY PLAN": "                                            Index Cond: (playlist_id = sp_1.playlist_id)"
  },
  {
    "QUERY PLAN": "                                            Filter: (NOT (hashed SubPlan 2))"
  },
  {
    "QUERY PLAN": "                                            Rows Removed by Filter: 10"
  },
  {
    "QUERY PLAN": "                                            Heap Fetches: 10"
  },
  {
    "QUERY PLAN": "                                            SubPlan 2"
  },
  {
    "QUERY PLAN": "                                              ->  CTE Scan on playlist_6_songs playlist_6_songs_1  (cost=0.00..0.42 rows=21 width=8) (actual time=0.001..0.002 rows=10 loops=1)"
  },
  {
    "QUERY PLAN": "                                ->  Hash  (cost=542.41..542.41 rows=26741 width=32) (actual time=10.450..10.451 rows=26741 loops=1)"
  },
  {
    "QUERY PLAN": "                                      Buckets: 32768  Batches: 1  Memory Usage: 1981kB"
  },
  {
    "QUERY PLAN": "                                      ->  Seq Scan on song s  (cost=0.00..542.41 rows=26741 width=32) (actual time=0.008..5.114 rows=26741 loops=1)"
  },
  {
    "QUERY PLAN": "                          ->  Hash  (cost=38.42..38.42 rows=1642 width=25) (actual time=0.558..0.558 rows=1682 loops=1)"
  },
  {
    "QUERY PLAN": "                                Buckets: 2048  Batches: 1  Memory Usage: 113kB"
  },
  {
    "QUERY PLAN": "                                ->  Seq Scan on album al  (cost=0.00..38.42 rows=1642 width=25) (actual time=0.006..0.258 rows=1682 loops=1)"
  },
  {
    "QUERY PLAN": "                    ->  Index Scan using artist_pkey on artist art  (cost=0.14..0.16 rows=1 width=15) (actual time=0.004..0.004 rows=1 loops=3)"
  },
  {
    "QUERY PLAN": "                          Index Cond: (id = s.artist_id)"
  },
  {
    "QUERY PLAN": "Planning Time: 2.946 ms"
  },
  {
    "QUERY PLAN": "Execution Time: 1835.582 ms"
  }
]
```

        2: Top Streams:
            - Old Time After Explain Analyze: 8509 ms
            - New Time: 833 ms

**Before**

```json
[
  {
    "QUERY PLAN": "Limit  (cost=395575.36..395575.39 rows=10 width=51) (actual time=8502.538..8503.186 rows=10 loops=1)"
  },
  {
    "QUERY PLAN": "  ->  Sort  (cost=395575.36..398367.41 rows=1116821 width=51) (actual time=8502.536..8503.183 rows=10 loops=1)"
  },
  {
    "QUERY PLAN": "        Sort Key: (row_number() OVER (?))"
  },
  {
    "QUERY PLAN": "        Sort Method: top-N heapsort  Memory: 26kB"
  },
  {
    "QUERY PLAN": "        ->  WindowAgg  (cost=351896.89..371441.26 rows=1116821 width=51) (actual time=8482.663..8498.958 rows=26740 loops=1)"
  },
  {
    "QUERY PLAN": "              ->  Sort  (cost=351896.89..354688.95 rows=1116821 width=43) (actual time=8481.636..8486.222 rows=26740 loops=1)"
  },
  {
    "QUERY PLAN": "                    Sort Key: (count(streams.stream_id)) DESC"
  },
  {
    "QUERY PLAN": "                    Sort Method: external merge  Disk: 1504kB"
  },
  {
    "QUERY PLAN": "                    ->  HashAggregate  (cost=168661.40..199461.23 rows=1116821 width=43) (actual time=8371.503..8468.310 rows=26740 loops=1)"
  },
  {
    "QUERY PLAN": "                          Group Key: streams.song_id, song.song_name, artist.artist_name"
  },
  {
    "QUERY PLAN": "                          Planned Partitions: 64  Batches: 65  Memory Usage: 4369kB  Disk Usage: 11016kB"
  },
  {
    "QUERY PLAN": "                          ->  Hash Join  (cost=882.75..113561.99 rows=1116821 width=43) (actual time=16.762..7736.484 rows=1080055 loops=1)"
  },
  {
    "QUERY PLAN": "                                Hash Cond: (song.artist_id = artist.id)"
  },
  {
    "QUERY PLAN": "                                ->  Hash Join  (cost=876.67..110555.62 rows=1116821 width=36) (actual time=16.685..7496.426 rows=1080055 loops=1)"
  },
  {
    "QUERY PLAN": "                                      Hash Cond: (streams.song_id = song.song_id)"
  },
  {
    "QUERY PLAN": "                                      ->  Seq Scan on streams  (cost=0.00..94521.16 rows=5774216 width=12) (actual time=0.010..6340.400 rows=5774216 loops=1)"
  },
  {
    "QUERY PLAN": "                                      ->  Hash  (cost=542.41..542.41 rows=26741 width=28) (actual time=16.580..16.581 rows=26741 loops=1)"
  },
  {
    "QUERY PLAN": "                                            Buckets: 32768  Batches: 1  Memory Usage: 1877kB"
  },
  {
    "QUERY PLAN": "                                            ->  Seq Scan on song  (cost=0.00..542.41 rows=26741 width=28) (actual time=0.008..9.036 rows=26741 loops=1)"
  },
  {
    "QUERY PLAN": "                                ->  Hash  (cost=3.81..3.81 rows=181 width=15) (actual time=0.066..0.067 rows=181 loops=1)"
  },
  {
    "QUERY PLAN": "                                      Buckets: 1024  Batches: 1  Memory Usage: 17kB"
  },
  {
    "QUERY PLAN": "                                      ->  Seq Scan on artist  (cost=0.00..3.81 rows=181 width=15) (actual time=0.009..0.031 rows=181 loops=1)"
  },
  {
    "QUERY PLAN": "Planning Time: 1.086 ms"
  },
  {
    "QUERY PLAN": "Execution Time: 8509.235 ms"
  }
]
```

**After**

```json
[
  {
    "QUERY PLAN": "Limit  (cost=349333.32..349333.35 rows=10 width=51) (actual time=830.101..830.106 rows=10 loops=1)"
  },
  {
    "QUERY PLAN": "  ->  Sort  (cost=349333.32..352125.37 rows=1116821 width=51) (actual time=830.100..830.104 rows=10 loops=1)"
  },
  {
    "QUERY PLAN": "        Sort Key: (row_number() OVER (?))"
  },
  {
    "QUERY PLAN": "        Sort Method: top-N heapsort  Memory: 26kB"
  },
  {
    "QUERY PLAN": "        ->  WindowAgg  (cost=305654.85..325199.22 rows=1116821 width=51) (actual time=810.133..825.827 rows=26740 loops=1)"
  },
  {
    "QUERY PLAN": "              ->  Sort  (cost=305654.85..308446.91 rows=1116821 width=43) (actual time=810.123..814.093 rows=26740 loops=1)"
  },
  {
    "QUERY PLAN": "                    Sort Key: (count(streams.stream_id)) DESC"
  },
  {
    "QUERY PLAN": "                    Sort Method: external merge  Disk: 1504kB"
  },
  {
    "QUERY PLAN": "                    ->  HashAggregate  (cost=122419.36..153219.19 rows=1116821 width=43) (actual time=755.727..797.531 rows=26740 loops=1)"
  },
  {
    "QUERY PLAN": "                          Group Key: streams.song_id, song.song_name, artist.artist_name"
  },
  {
    "QUERY PLAN": "                          Planned Partitions: 64  Batches: 65  Memory Usage: 4369kB  Disk Usage: 11528kB"
  },
  {
    "QUERY PLAN": "                          ->  Nested Loop  (cost=0.59..67319.95 rows=1116821 width=43) (actual time=0.034..356.230 rows=1080055 loops=1)"
  },
  {
    "QUERY PLAN": "                                ->  Nested Loop  (cost=0.15..1232.96 rows=26741 width=35) (actual time=0.023..21.455 rows=26741 loops=1)"
  },
  {
    "QUERY PLAN": "                                      ->  Seq Scan on song  (cost=0.00..542.41 rows=26741 width=28) (actual time=0.012..8.535 rows=26741 loops=1)"
  },
  {
    "QUERY PLAN": "                                      ->  Memoize  (cost=0.15..0.17 rows=1 width=15) (actual time=0.000..0.000 rows=1 loops=26741)"
  },
  {
    "QUERY PLAN": "                                            Cache Key: song.artist_id"
  },
  {
    "QUERY PLAN": "                                            Cache Mode: logical"
  },
  {
    "QUERY PLAN": "                                            Hits: 26582  Misses: 159  Evictions: 0  Overflows: 0  Memory Usage: 19kB"
  },
  {
    "QUERY PLAN": "                                            ->  Index Scan using artist_pkey on artist  (cost=0.14..0.16 rows=1 width=15) (actual time=0.002..0.002 rows=1 loops=159)"
  },
  {
    "QUERY PLAN": "                                                  Index Cond: (id = song.artist_id)"
  },
  {
    "QUERY PLAN": "                                ->  Index Only Scan using idx_streams_composite on streams  (cost=0.43..2.05 rows=42 width=12) (actual time=0.003..0.008 rows=40 loops=26741)"
  },
  {
    "QUERY PLAN": "                                      Index Cond: (song_id = song.song_id)"
  },
  {
    "QUERY PLAN": "                                      Heap Fetches: 24065"
  },
  {
    "QUERY PLAN": "Planning Time: 1.228 ms"
  },
  {
    "QUERY PLAN": "Execution Time: 833.099 ms"
  }
]
```

        3: Remove Song From Playlist:
            - Old Time After Explain Analyze: 2928 ms
            - New Time: 9 ms

**Before**

```json
[
  {
    "QUERY PLAN": "Delete on song_playlist  (cost=2.94..107430.03 rows=0 width=0) (actual time=2928.776..2928.779 rows=0 loops=1)"
  },
  {
    "QUERY PLAN": "  ->  Nested Loop  (cost=2.94..107430.03 rows=1 width=18) (actual time=2928.775..2928.778 rows=0 loops=1)"
  },
  {
    "QUERY PLAN": "        ->  Hash Join  (cost=2.52..107380.67 rows=112 width=20) (actual time=246.982..2927.401 rows=43 loops=1)"
  },
  {
    "QUERY PLAN": "              Hash Cond: (song_playlist.song_id = song.song_id)"
  },
  {
    "QUERY PLAN": "              ->  Seq Scan on song_playlist  (cost=0.00..93268.25 rows=5374725 width=22) (actual time=1.148..2461.892 rows=5374724 loops=1)"
  },
  {
    "QUERY PLAN": "              ->  Hash  (cost=2.51..2.51 rows=1 width=10) (actual time=0.031..0.032 rows=1 loops=1)"
  },
  {
    "QUERY PLAN": "                    Buckets: 1024  Batches: 1  Memory Usage: 9kB"
  },
  {
    "QUERY PLAN": "                    ->  Index Scan using idx_song_name on song  (cost=0.29..2.51 rows=1 width=10) (actual time=0.023..0.023 rows=1 loops=1)"
  },
  {
    "QUERY PLAN": "                          Index Cond: (song_name = 'The Code (feat. Juicy J, Lola Monroe, Chevy Woods)'::text)"
  },
  {
    "QUERY PLAN": "        ->  Index Scan using user_playlist_pkey on user_playlist  (cost=0.42..0.44 rows=1 width=14) (actual time=0.029..0.029 rows=0 loops=43)"
  },
  {
    "QUERY PLAN": "              Index Cond: (playlist_id = song_playlist.playlist_id)"
  },
  {
    "QUERY PLAN": "              Filter: (playlist_name = 'u10p10'::text)"
  },
  {
    "QUERY PLAN": "              Rows Removed by Filter: 1"
  },
  {
    "QUERY PLAN": "Planning Time: 1.277 ms"
  },
  {
    "QUERY PLAN": "Execution Time: 2928.919 ms"
  }
]
```

**After**

```json
[
  {
    "QUERY PLAN": "Delete on song_playlist  (cost=1.14..3133.52 rows=0 width=0) (actual time=9.317..9.318 rows=0 loops=1)"
  },
  {
    "QUERY PLAN": "  ->  Nested Loop  (cost=1.14..3133.52 rows=1 width=18) (actual time=9.316..9.317 rows=0 loops=1)"
  },
  {
    "QUERY PLAN": "        ->  Index Scan using idx_song_name on song  (cost=0.29..2.51 rows=1 width=10) (actual time=0.021..0.022 rows=1 loops=1)"
  },
  {
    "QUERY PLAN": "              Index Cond: (song_name = 'The Code (feat. Juicy J, Lola Monroe, Chevy Woods)'::text)"
  },
  {
    "QUERY PLAN": "        ->  Nested Loop  (cost=0.85..3131.01 rows=1 width=20) (actual time=9.291..9.292 rows=0 loops=1)"
  },
  {
    "QUERY PLAN": "              ->  Index Scan using idx_user_playlist_playlist_id_playlist_name on user_playlist  (cost=0.42..3128.35 rows=1 width=14) (actual time=0.013..9.259 rows=1 loops=1)"
  },
  {
    "QUERY PLAN": "                    Index Cond: (playlist_name = 'u10p10'::text)"
  },
  {
    "QUERY PLAN": "              ->  Index Scan using idx_song_playlist_playlist_id_song_id on song_playlist  (cost=0.43..2.65 rows=1 width=22) (actual time=0.031..0.031 rows=0 loops=1)"
  },
  {
    "QUERY PLAN": "                    Index Cond: ((playlist_id = user_playlist.playlist_id) AND (song_id = song.song_id))"
  },
  {
    "QUERY PLAN": "Planning Time: 1.407 ms"
  },
  {
    "QUERY PLAN": "Execution Time: 9.425 ms"
  }
]
```

    Fixes:
        1:
            -Command:
                CREATE INDEX idx_song_playlist_playlist_id_song_id ON song_playlist(playlist_id, song_id);
                CREATE INDEX idx_user_playlist_user_id_playlist_id_playlist_name ON user_playlist(user_id, playlist_id, playlist_name);
                CREATE INDEX idx_users_user_id ON users(user_id);
            -Explanation:
                Boosts performance by allowing the database to quickly locate and join relevant records based on the playlist_id, song_id.

        2:
            -Command:
                CREATE INDEX idx_streams_song_id ON streams(song_id);
                CREATE INDEX idx_streams_composite ON streams(song_id, stream_id);
            -Explanation:
                Reduced the time needed for the database to search and aggregate the streams table based on the song_id and stream_id columns, thereby speeding up the JOIN and GROUP BY operations.

        3:
            -Command:
                CREATE INDEX idx_user_playlist_playlist_id_playlist_name ON user_playlist(playlist_id, playlist_name);
                CREATE INDEX idx_song_playlist_playlist_id_song_id ON song_playlist(playlist_id, song_id);
                CREATE INDEX idx_song_song_id_song_name ON song(song_id, song_name);
            -Explanation:
                Boosts performance by enabling faster searches and joins on the relevant columns used in the DELETE query's JOIN and WHERE conditions.

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
