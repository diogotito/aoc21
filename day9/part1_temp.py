import itertools
import pprint

BEFORE_0 = ord("0") - 1  # Subtracting this to a cell's ord() gives its risk level

lines = open("input.txt").readlines()

# My heightmap will be padded with ':' characters because in ASCII ':' > '0'
size = len(lines) + 2

heightmap = [":" * size, *(":" + line.rstrip() + ":" for line in lines), ":" * size]


def iter_neighbours(heightmap):
    coords = itertools.product(range(1, size - 1), range(1, size - 1))
    for x, y in coords:
        yield (
            heightmap[y][x],
            heightmap[y - 1][x],
            heightmap[y][x + 1],
            heightmap[y + 1][x],
            heightmap[y][x - 1],
        )


print(
    sum(
        ord(cell) - BEFORE_0  # Risk level for cell
        for cell, *neighbours in iter_neighbours(heightmap)
        if all(neighbour > cell for neighbour in neighbours)
    )
)
