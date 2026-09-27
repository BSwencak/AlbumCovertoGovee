def print_color_block(name, rgb):
    r, g, b = rgb
    block = f"\033[48;2;{r};{g};{b}m   \033[0m"
    print(f"{name}: {rgb} {block}")
