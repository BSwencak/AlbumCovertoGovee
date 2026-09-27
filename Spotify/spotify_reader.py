import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from PIL import Image
from io import BytesIO


# Spotify authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="user-read-currently-playing user-read-playback-state"
    )
)

# Fetch album art
def get_album_image():
    current = sp.current_playback()
    if not current or not current.get("item"):
        print("No song playing")
        return None

    images = current["item"]["album"]["images"]
    url = images[0]["url"]  # highest resolution
    img_data = requests.get(url).content
    return Image.open(BytesIO(img_data)).convert("RGB")