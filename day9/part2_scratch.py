def print_basin(basin):
    print("," + "_" * width + ".", end="\n|")
    for y, x in itertools.product(range(height), range(width)):
        print(
            heightmap[y][x] if (x, y) in basin else " ",
            end="" if x < width - 1 else "|\n|" if y < height - 1 else "|\n",
        )
    print("`" + "¯" * width + "´")
