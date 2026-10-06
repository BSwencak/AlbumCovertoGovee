import os
import time
from dotenv import load_dotenv
from Govee.govee_client import get_devices, set_color

load_dotenv()

# Quadrant → Lamp mapping using your real device IDs
QUADRANT_TO_LAMP = {
    "top_left": os.getenv("LAMP_TOP"),
    "top_right": os.getenv("LAMP_2"),
    "bottom_left": os.getenv("LAMP_SIDE"),
    "bottom_right": os.getenv("LAMP_1")
}

last_colors = {}


def fade_color(client, lamp_name, old_rgb, new_rgb, steps=5, delay=0.01):
    """Fade smoothly from old_rgb to new_rgb."""
    old_r, old_g, old_b = old_rgb
    new_r, new_g, new_b = new_rgb

    for i in range(steps):
        t = i / steps
        r = int(old_r + (new_r - old_r) * t)
        g = int(old_g + (new_g - old_g) * t)
        b = int(old_b + (new_b - old_b) * t)

        set_color(client, lamp_name, (r, g, b))
        time.sleep(delay)

def update_lamps(client, colors):
    get_devices(client)  # Ensure devices are discovered before updating
    """Update each lamp to its corresponding quadrant color with fading."""
    for quadrant, rgb in colors.items():
        lamp_name = QUADRANT_TO_LAMP.get(quadrant)
        if not lamp_name:
            print(f"No lamp mapped for quadrant '{quadrant}'")
            continue

        # If first time updating this lamp
        if lamp_name not in last_colors:
            print(f"Setting initial color for {quadrant}: {rgb}")
            set_color(client, lamp_name, rgb)
            last_colors[lamp_name] = rgb
            continue

        old_rgb = last_colors[lamp_name]



        print(f"Fading {quadrant} lamp ({lamp_name}) from {old_rgb} → {rgb}")
        fade_color(client, lamp_name, old_rgb, rgb)

        last_colors[lamp_name] = rgb