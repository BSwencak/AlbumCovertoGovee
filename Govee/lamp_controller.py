import os
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
