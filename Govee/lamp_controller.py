import os
import time
from dotenv import load_dotenv
from Govee.govee_client import set_color

load_dotenv()

# Quadrant → Lamp mapping using your real device IDs
QUADRANT_TO_LAMP = {
    "top_left": os.getenv("LAMP_1"),
    "top_right": os.getenv("LAMP_2"),
    "bottom_left": os.getenv("LAMP_3"),
    "bottom_right": os.getenv("LAMP_4")
}

# Cache to avoid redundant updates
last_colors = {}

def is_similar(c1, c2, tolerance=10):
    """Check if two RGB colors are close enough to skip updating."""
    return all(abs(a - b) < tolerance for a, b in zip(c1, c2))

def fade_color(client, lamp_id, old_rgb, new_rgb, steps=20, delay=0.01):
    """Fade smoothly from old_rgb to new_rgb."""
    old_r, old_g, old_b = old_rgb
    new_r, new_g, new_b = new_rgb

    for i in range(steps):
        t = i / steps
        r = int(old_r + (new_r - old_r) * t)
        g = int(old_g + (new_g - old_g) * t)
        b = int(old_b + (new_b - old_b) * t)

        set_color(client, lamp_id, (r, g, b))
        time.sleep(delay)

def update_lamps(client, colors):
    """Update each lamp to its corresponding quadrant color with fading."""
    for quadrant, rgb in colors.items():
        lamp_id = QUADRANT_TO_LAMP.get(quadrant)
        if not lamp_id:
            print(f"No lamp mapped for quadrant '{quadrant}'")
            continue

        # If first time updating this lamp
        if lamp_id not in last_colors:
            print(f"Setting initial color for {quadrant}: {rgb}")
            set_color(client, lamp_id, rgb)
            last_colors[lamp_id] = rgb
            continue

        old_rgb = last_colors[lamp_id]

        # Skip tiny changes
        if is_similar(old_rgb, rgb):
            continue

        print(f"Fading {quadrant} lamp ({lamp_id}) from {old_rgb} → {rgb}")
        fade_color(client, lamp_id, old_rgb, rgb)

        last_colors[lamp_id] = rgb




























'''import os
from dotenv import load_dotenv
from Govee.govee_client import set_color

load_dotenv()

# Quadrant → Lamp mapping using your real device IDs
QUADRANT_TO_LAMP = {
    "top_left": os.getenv("LAMP_TOP"),       # Lamp Top
    "top_right": os.getenv("LAMP_2"),      # Lamp 2
    "bottom_left": os.getenv("LAMP_SIDE"),    # Lamp Side
    "bottom_right": os.getenv("LAMP_1")    # Lamp 1
}

# Cache to avoid redundant updates
last_colors = {}

def is_similar(c1, c2, tolerance=10):
    """Check if two RGB colors are close enough to skip updating."""
    return all(abs(a - b) < tolerance for a, b in zip(c1, c2))

def update_lamps(client, colors):
    """
    Update each lamp to its corresponding quadrant color.
    
    colors: dict like:
        {
            "top_left": (r,g,b),
            "top_right": (r,g,b),
            "bottom_left": (r,g,b),
            "bottom_right": (r,g,b)
        }
    """

    for quadrant, rgb in colors.items():
        lamp_id = QUADRANT_TO_LAMP.get(quadrant)

        if not lamp_id:
            print(f"No lamp mapped for quadrant '{quadrant}'")
            continue

        # Only update if color changed significantly
        if lamp_id not in last_colors or not is_similar(last_colors[lamp_id], rgb):
            print(f"Updating {quadrant} lamp ({lamp_id}) to color: {rgb}")
            set_color(client, lamp_id, rgb)
            last_colors[lamp_id] = rgb
'''