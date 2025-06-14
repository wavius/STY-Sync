# StoY-Sync
Simple python script that syncs Spotify and YT Music playlists. 

### Usage

1. **Clone the repo and install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   - Copy `.env_example` to `.env`:
     ```bash
     cp .env_example .env
     ```
   - Fill in your own Spotify and YouTube OAuth credentials inside `.env`.

3. **Authenticate YouTube Music (one-time setup):**
   ```bash
   python setup.py
   ```

4. **Sync selected Spotify playlists to YouTube Music:**
   ```bash
   python main.py
   ```
   - You'll be shown a numbered list of your Spotify playlists.
   - Enter the numbers (e.g. `0, 2`) to sync only those.

5. **(Optional) Delete all YouTube Music playlists:**
   ⚠️ **This is irreversible!**
   ```bash
   python delete.py
   ```
