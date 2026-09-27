import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from PIL import Image
from io import BytesIO

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="user-read-currently-playing user-read-playback-state"
    )
)

def get_current_track_id():
    current = sp.current_playback()
    if current and current.get("item"):
        return current["item"]["id"]
    return None

def get_current_track_name():
    current = sp.current_playback()
    if current and current.get("item"):
        return current["item"]["name"]
    return None

def get_album_image():
    current = sp.current_playback()
    if not current or not current.get("item"):
        return None

    url = current["item"]["album"]["images"][0]["url"]
    img_data = requests.get(url).content
    return Image.open(BytesIO(img_data)).convert("RGB")

def get_current_album_id():
    current = sp.current_playback()
    if current and current.get("item"):
        return current["item"]["album"]["id"]
    return None

def get_current_album_name():
    current = sp.current_playback()
    if current and current.get("item"):
        return current["item"]["album"]["name"]
    return None