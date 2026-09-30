import time
import os
# Spotify
from Spotify.spotify_reader import (
    get_current_track_id,
    get_current_track_name,
    get_album_image,
    get_current_album_id,
    get_current_album_name
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

while True:
    track_id = get_current_track_id()
    album_id = get_current_album_id()

    if track_id and track_id != last_track_id:
        last_track_id = track_id

        print(f"\nNew song detected: {get_current_track_name()}")

        img = get_album_image()
        if img:
            # Extract colors for all quadrants
            colors = quadrant_dominant_colors(img)

            # Print quadrant colors for debugging
            for name, rgb in colors.items():
                print_color_block(f"{name}: {rgb}", rgb)


    if album_id and album_id != last_album_id:
        print(f"New album detected: {get_current_album_name()}")
        # Update lamps (each lamp gets its own quadrant color)
        update_lamps(client, colors)
        print("LAMPS UPDATED")
        last_album_id = album_id

    time.sleep(1)
