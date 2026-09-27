import numpy as np

def split_quadrants(img):
    w, h = img.size
    arr = np.array(img)

    return {
        "top_left":     arr[0:h//2, 0:w//2],
        "top_right":    arr[0:h//2, w//2:w],
        "bottom_left":  arr[h//2:h, 0:w//2],
        "bottom_right": arr[h//2:h, w//2:w]
    }
