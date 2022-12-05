import itertools
import pprint

BEFORE_0 = ord("0") - 1  # Subtracting this to a cell's ord() gives its risk level

lines = open("input_goucha.txt").readlines()

# My heightmap will be padded with ':' characters because in ASCII ':' > '0'
size = len(lines) + 2
heightmap = [":" * size, *(f":{line.rstrip()}:" for line in lines), ":" * size]


def iter_neighbours(heightmap):
    """Takes a padded heightmap and yields all the proper cells along with their
    four neighbours (which can be in the frame)
    """
    coords = itertools.product(range(1, size - 1), range(1, size - 1))
    for x, y in coords:
        yield (
            heightmap[y][x],
            heightmap[y - 1][x],  # Up
            heightmap[y][x + 1],  # Right
            heightmap[y + 1][x],  # Down
            heightmap[y][x - 1],  # Left
        )


# such beautiful
# print(
#    sum(
#        ord(cell) - BEFORE_0  # Risk level for cell
#        for cell, *neighbours in iter_neighbours(heightmap)
#        if all(adjacent > cell for adjacent in neighbours)
#    )
# )

for i, (cell, *neighbours) in zip(range(100 * 100), iter_neighbours(heightmap)):
    print(
        cell if all(adjacent > cell for adjacent in neighbours) else ".",
        end="" if (i + 1) % 100 else "\n",
    )
