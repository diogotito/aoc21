import itertools
import functools
import operator

lines = open("input.txt").readlines()

heightmap = [[int(digit) for digit in line.rstrip()] for line in lines]
width = len(heightmap[0])
height = len(heightmap)


def iter_neighbours(x, y):
    if y > 0:
        yield (x, y - 1)  # Up
    if x < width - 1:
        yield (x + 1, y)  # Right
    if y < height - 1:
        yield (x, y + 1)  # Down
    if x > 0:
        yield (x - 1, y)  # Left


all_pos = itertools.product(range(width), range(height))
to_visit = set((x, y) for x, y in all_pos if heightmap[y][x] != 9)


def walk(pos, basin):
    basin.add(pos)
    to_visit.remove(pos)
    for adj_pos in iter_neighbours(*pos):
        if adj_pos in to_visit:
            walk(adj_pos, basin)
    return basin


basins = []


while to_visit:
    starting_pos = next(iter(to_visit))
    basins.append(walk(pos=starting_pos, basin=set()))

basins.sort(key=len, reverse=True)
answer = functools.reduce(operator.mul, map(len, basins[:3]))

print(answer)  # Your puzzle answer was 1317792.
