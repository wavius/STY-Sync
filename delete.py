import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from ytmusicapi import YTMusic, OAuthCredentials
from dotenv import load_dotenv
import os

load_dotenv()

# Setup YTMusic
ytmusic = YTMusic("oauth.json", oauth_credentials=OAuthCredentials(
    client_id=os.getenv("YT_CLIENT_ID"),
    client_secret=os.getenv("YT_CLIENT_SECRET")
))

# Get your playlists
playlists = ytmusic.get_library_playlists()
print(f"🧨 Found {len(playlists) - 2} playlists to delete.")

# Delete each playlist
for pl in playlists:
    if pl['title'] != "Liked Music" and pl['title'] != "Episodes for Later":
        print(f"🗑️ Deleting: {pl['title']}")
        ytmusic.delete_playlist(pl['playlistId'])

print("✅ All playlists deleted.")