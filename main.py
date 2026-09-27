import time
from Spotify.spotify_reader import (
    get_current_track_id,
    get_current_track_name,
    get_album_image
)
from Image_Processing.quadrant_dominant import quadrant_dominant_colors
from Utils.print_color import print_color_block

last_track_id = None

while True:
    track_id = get_current_track_id()

    if track_id and track_id != last_track_id:
        last_track_id = track_id

        print(f"\nNew song detected: {get_current_track_name()}")

        img = get_album_image()
        if img:
            colors = quadrant_dominant_colors(img)

            for name, rgb in colors.items():
                print_color_block(name, rgb)

    time.sleep(1)
