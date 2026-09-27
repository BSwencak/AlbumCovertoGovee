import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import time
import colorsys

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

# Dominant color using histogram binning (no sklearn)
def dominant_color(rgb_array, bins=16):
    pixels = rgb_array.reshape(-1, 3)

    # Quantize
    quantized = (pixels // (256 // bins)).astype(int)
    unique, counts = np.unique(quantized, axis=0, return_counts=True)

    # Convert quantized colors back to full RGB
    scale = 256 // bins
    colors = []
    for (r_bin, g_bin, b_bin), count in zip(unique, counts):
        r = int(r_bin * scale + scale // 2)
        g = int(g_bin * scale + scale // 2)
        b = int(b_bin * scale + scale // 2)

        # Convert to HSV for filtering
        hsv = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        h, s, v = hsv

        # FILTER RULES:
        # Skip very dark colors
        if v < 0.15:
            continue

        # Skip low-saturation colors (grayish)
        if s < 0.20:
            continue

        # Skip near-black or near-white
        if (r < 40 and g < 40 and b < 40) or (r > 220 and g > 220 and b > 220):
            continue

        colors.append((count, (r, g, b)))

    # If everything was filtered out, fall back to brightest color
    if not colors:
        brightest = max(unique, key=lambda c: sum(c))
        r = int(brightest[0] * scale + scale // 2)
        g = int(brightest[1] * scale + scale // 2)
        b = int(brightest[2] * scale + scale // 2)
        return r, g, b

    # Pick the most frequent remaining color
    colors.sort(reverse=True, key=lambda x: x[0])
    return colors[0][1]


# Get dominant color per quadrant
def quadrant_dominant_colors(img: Image.Image):
    w, h = img.size
    img_np = np.array(img)

    quadrants = {
        "top_left":     img_np[0:h//2, 0:w//2],
        "top_right":    img_np[0:h//2, w//2:w],
        "bottom_left":  img_np[h//2:h, 0:w//2],
        "bottom_right": img_np[h//2:h, w//2:w]
    }

    colors = {}
    for name, q in quadrants.items():
        colors[name] = dominant_color(q)

    return colors

# Print color swatch in terminal
def print_color_block(name, rgb):
    r, g, b = rgb
    block = f"\033[48;2;{r};{g};{b}m   \033[0m"
    print(f"{name}: {rgb} {block}")

# Live loop: update when song changes
last_track_id = None

while True:
    current = sp.current_playback()

    if current and current.get("item"):
        track_id = current["item"]["id"]

        if track_id != last_track_id:
            last_track_id = track_id
            print(f"\nNew song detected: {current['item']['name']}")

            img = get_album_image()
            if img:
                colors = quadrant_dominant_colors(img)
                for name, rgb in colors.items():
                    print_color_block(name, rgb)

    time.sleep(1)  # check once per second
