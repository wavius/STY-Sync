import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic, OAuthCredentials

load_dotenv()

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="playlist-read-private playlist-read-collaborative"
))

ytmusic = YTMusic("oauth.json", oauth_credentials=OAuthCredentials(
    client_id=os.getenv("YT_CLIENT_ID"),
    client_secret=os.getenv("YT_CLIENT_SECRET")
))

# get spotify playlists
spotify_playlists = sp.current_user_playlists()['items']
print("📋 Spotify Playlists:")
for i, pl in enumerate(spotify_playlists):
    print(f"{i}: {pl['name']}")

# input on which playlists to sync
indices = input("Enter playlist numbers to sync (comma-separated): ")
selected_indices = {int(i.strip()) for i in indices.split(",") if i.strip().isdigit()}

# get existing yt playlists
yt_playlists = {pl['title']: pl['playlistId'] for pl in ytmusic.get_library_playlists()}

# sync playlists
for i, pl in enumerate(spotify_playlists):
    if i not in selected_indices:
        continue

    sp_name = pl['name']
    yt_name = f"{sp_name} (from Spotify)"
    print(f"\n🎵 Syncing: {sp_name}")

    

    if yt_name in yt_playlists:
        yt_id = yt_playlists[yt_name]
        print(f"🔁 Using existing YT playlist: {yt_name}")
    else:
        yt_id = ytmusic.create_playlist(yt_name, f"Imported from Spotify: {sp_name}")
        print(f"🆕 Created YT playlist: {yt_name}")

        # wait for playlist to be created
        import time
        for attempt in range(10):
            try:
                _ = ytmusic.get_playlist(yt_id)
                break
            except Exception:
                print(f"⌛ Waiting for playlist to be available... (Attempt {attempt + 1})")
                time.sleep(1)
        else:
            print("❌ Failed to access the newly created playlist.")
            continue


    video_ids_to_remove = []

    # remove tracks in yt music playlist not in spotify playlist
    yt_existing = ytmusic.get_playlist(yt_id, limit=None)['tracks']
    tracks = sp.playlist_tracks(pl['id'])
    spotify_existing = []

    while tracks:
        for item in tracks['items']:
            track = item.get('track')
            if not track:
                continue
            name = track['name']
            artists = ', '.join(a['name'] for a in track['artists'])
            spotify_existing.append(name)
       
        tracks = sp.next(tracks) if tracks['next'] else None

    for track in yt_existing:
        if track['title'] in spotify_existing:
            continue
        
        video_ids_to_remove.append({
            "videoId": track['videoId'],
            "setVideoId": track['setVideoId']
        })
        name = track['title']
        artists = ', '.join(a['name'] for a in track['artists'])
        print(f"🗑️  Removing: {name} by {artists}")


    if video_ids_to_remove:
        ytmusic.remove_playlist_items(yt_id, video_ids_to_remove)
        print(f"Removed {len(video_ids_to_remove)} tracks from {yt_name}")
    else:
        print("Nothing to remove.")


    video_ids_to_add = []

    tracks = sp.playlist_tracks(pl['id'])
    while tracks:
        for item in tracks['items']:
            track = item.get('track')
            if not track:
                continue
            name = track['name']
            artists = ', '.join(a['name'] for a in track['artists'])

            existing = False
            for track in yt_existing:
                if track['title'] == name:
                    existing = True
                    continue

            if existing:
                continue    

            query = f"{name} by {artists}"
            results = ytmusic.search(query, filter="songs")
            if results:
                video_ids_to_add.append(results[0]['videoId'])
                print(f"✅ Queued: {name} by {artists}")
            else:
                print(f"❌ Not found: {name} by {artists}")

        tracks = sp.next(tracks) if tracks['next'] else None
    video_ids_to_add = [vid for vid in video_ids_to_add if isinstance(vid, str) and len(vid) > 0]
    if video_ids_to_add:
        ytmusic.add_playlist_items(yt_id, video_ids_to_add, duplicates=False)
        print(f"Added {len(video_ids_to_add)} new tracks to {yt_name}")
    else:
        print("Nothing new to add.")

    

