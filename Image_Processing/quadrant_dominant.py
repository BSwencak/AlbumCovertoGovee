from .quadrant_split import split_quadrants
from .color_extract import dominant_color

def quadrant_dominant_colors(img):
    quads = split_quadrants(img)
    return {name: dominant_color(q) for name, q in quads.items()}
