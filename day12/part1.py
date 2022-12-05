import itertools
import re

lines = [line.rstrip() for line in open('input.txt').readlines()]

end_of_points = next(i for i, line in enumerate(lines) if not line)
points = {tuple(map(int, line.split(','))) for line in lines[:end_of_points]}
folds = lines[end_of_points + 1:]


def fold_left(pos):
    global points
    new_points = set()
    for x, y in points:
        new_points.add((x if x <= pos else pos - (x - pos), y))
    points = new_points


def fold_up(pos):
    global points
    new_points = set()
    for x, y in points:
        new_points.add((x, y if y <= pos else pos - (y - pos)))
    points = new_points


FOLD_RE = re.compile(r"fold along ([xy])=(\d+)")

for fold_instruction in folds:
    fold_dir, pos = FOLD_RE.match(fold_instruction).groups()
    {'x': fold_left, 'y': fold_up}[fold_dir](int(pos))

import random

for r, c in itertools.product(range(-1, 7), range(-5, 52)):
    print('  ▒▓█████'[r] if (c, r) in points else '░ '[random.randint(0, (r + 1) ** 2) > 7],
          end='\n' if c == 51 else '')
