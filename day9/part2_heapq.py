import itertools
import functools
import operator
import heapq

lines = open("input.txt").readlines()

heightmap = [[int(digit) for digit in line.rstrip()] for line in lines]
width = len(heightmap[0])
height = len(heightmap)


def iter_neighbours(x, y):
    if y > 0         : yield (x, y - 1)  # Up
    if x < width - 1 : yield (x + 1, y)  # Right
    if y < height - 1: yield (x, y + 1)  # Down
    if x > 0         : yield (x - 1, y)  # Left


def walk(pos, basin):
    basin.add(pos)
    for neighbour in iter_neighbours(*pos):
        if neighbour in to_visit:
            to_visit.remove(neighbour)
            walk(neighbour, basin)
    return basin


basins = []

all_pos = itertools.product(range(width), range(height))
to_visit = set((x, y) for x, y in all_pos if heightmap[y][x] != 9)

while to_visit:
    basins.append(walk(pos=to_visit.pop(), basin=set()))

three_largest = heapq.nlargest(3, basins, key=len)
answer = functools.reduce(operator.mul, map(len, three_largest))

print(answer)  # Your puzzle answer was 1317792.
