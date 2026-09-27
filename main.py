import time

# Spotify
from Spotify.spotify_reader import (
    get_current_track_id,
    get_current_track_name,
    get_album_image
)

# Image processing
from Image_Processing.quadrant_dominant import quadrant_dominant_colors

# Govee
from Govee.govee_client import init_govee
from Govee.lamp_controller import update_lamps


# Initialize Govee client
client = init_govee()

last_track_id = None

while True:
    track_id = get_current_track_id()

    if track_id and track_id != last_track_id:
        last_track_id = track_id

        print(f"\nNew song detected: {get_current_track_name()}")

        img = get_album_image()
        if img:
            # Extract colors for all quadrants
            colors = quadrant_dominant_colors(img)

            # Print quadrant colors for debugging
            for name, rgb in colors.items():
                print(f"{name}: {rgb}")

            # Update lamps (each lamp gets its own quadrant color)
            update_lamps(client, colors)

    time.sleep(1)
