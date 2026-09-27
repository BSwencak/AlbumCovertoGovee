

def split_quadrants(rgb_array):             
    h, w, _ = rgb_array.shape
    top_left = rgb_array[0:h//2, 0:w//2]
    top_right = rgb_array[0:h//2, w//2:w]
    bottom_left = rgb_array[h//2:h, 0:w//2]
    bottom_right = rgb_array[h//2:h, w//2:w]
    return top_left, top_right, bottom_left, bottom_right
