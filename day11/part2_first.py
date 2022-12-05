import itertools

octopuses = [[int(o) for o in line.rstrip()] for line in open("input.txt")]
size = len(octopuses)


def iter_neighbours(x, y):
    if y > 0:
        yield x, y - 1  # Up
    if x < size - 1:
        yield x + 1, y  # Right
    if y < size - 1:
        yield x, y + 1  # Down
    if x > 0:
        yield x - 1, y  # Left
    if y > 0 and x < size - 1:
        yield x + 1, y - 1
    if y > 0 and x > 0:
        yield x - 1, y - 1
    if y < size - 1 and x > 0:
        yield x - 1, y + 1
    if y < size - 1 and x < size - 1:
        yield x + 1, y + 1


for step in itertools.count(1):
    flashed_this_step = set()
    to_flash = set()

    for r, c in itertools.product(range(size), range(size)):
        octopuses[r][c] += 1
        if octopuses[r][c] > 9:
            to_flash.add((r, c))

    # "Recursively" flash octopuses with energy level over 9
    while to_flash:
        (r, c) = to_flash.pop()
        if (r, c) in flashed_this_step:
            continue
        flashed_this_step.add((r, c))
        for nr, nc in iter_neighbours(r, c):
            octopuses[nr][nc] += 1
            if octopuses[nr][nc] > 9:
                to_flash.add((nr, nc))

    if len(flashed_this_step) == 100:
        print(step)
        break

    for r, c in flashed_this_step:
        octopuses[r][c] = 0
