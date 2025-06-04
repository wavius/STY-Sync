from dotenv import load_dotenv
import os
from ytmusicapi import setup_oauth

load_dotenv()

setup_oauth(os.getenv("YT_CLIENT_ID"), os.getenv("YT_CLIENT_SECRET"), "oauth.json")