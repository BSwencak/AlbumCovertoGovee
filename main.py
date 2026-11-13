import time
import os
import requests
from PIL import Image
from io import BytesIO
# Spotify
from Spotify.spotify_reader import (
    get_current_playback
)

# Image processing
from Image_Processing.quadrant_dominant import quadrant_dominant_colors

#Utils
from Utils.print_color import print_color_block

# Govee
from Govee.govee_client import init_govee
from Govee.lamp_controller import update_lamps


# Initialize Govee client
client = init_govee(os.getenv("GOVEE_API_KEY"))

last_track_id = None
last_album_id = None

PID_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "spotify.pid"
)

with open(PID_FILE, "w") as f:
    f.write(str(os.getpid()))

try:
    while True:
        current = get_current_playback()

        if current and current.get("item"):

            track_id = current["item"]["id"]
            album_id = current["item"]["album"]["id"]

            if track_id != last_track_id:
                last_track_id = track_id

                print(f"\nNew song detected: {current['item']['name']}")

                url = current["item"]["album"]["images"][0]["url"]
                img = Image.open(BytesIO(requests.get(url).content)).convert("RGB")

                colors = quadrant_dominant_colors(img)

            if album_id != last_album_id:
                print(f"New album detected: {current['item']['album']['name']}")

                update_lamps(client, colors)

                last_album_id = album_id

        time.sleep(1)

finally:
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)