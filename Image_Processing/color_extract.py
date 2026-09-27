import numpy as np
import colorsys

def dominant_color(rgb_array, bins=16):
    pixels = rgb_array.reshape(-1, 3)
    quantized = (pixels // (256 // bins)).astype(int)
    unique, counts = np.unique(quantized, axis=0, return_counts=True)

    scale = 256 // bins
    filtered = []

    for (r_bin, g_bin, b_bin), count in zip(unique, counts):
        r = int(r_bin * scale + scale // 2)
        g = int(g_bin * scale + scale // 2)
        b = int(b_bin * scale + scale // 2)

        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)

        if v < 0.15: continue
        if s < 0.20: continue
        if (r < 40 and g < 40 and b < 40): continue
        if (r > 220 and g > 220 and b > 220): continue

        filtered.append((count, (r, g, b)))

    if not filtered:
        brightest = max(unique, key=lambda c: sum(c))
        return (
            int(brightest[0] * scale + scale // 2),
            int(brightest[1] * scale + scale // 2),
            int(brightest[2] * scale + scale // 2)
        )

    filtered.sort(reverse=True, key=lambda x: x[0])
    return filtered[0][1]
