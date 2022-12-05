import collections
import re
import pprint

Line = collections.namedtuple('Line', ('x1','y1','x2','y2'))

def my_range(a, b):
    """range(), mas inclusivo e se a > b vai de cima para baixo"""
    direction = (a < b) - (a > b)
    return range(a, b + direction, direction) if a != b else range(a, a + 1)


def iter_line(line):
    x1, y1, x2, y2 = line
    
    # Horizontal line
    if x1 == x2:
        for y in my_range(y1, y2):
            yield (x1, y)

    # Vertical line
    if y1 == y2:
        for x in my_range(x1, x2):
            yield (x, y1)


point_counter = collections.Counter()


for line in open('input.txt'):
    digits = re.findall(r"\d+", line)
    [x1, x2, y1, y2] = [int(n) for n in digits]
    line = Line(x1, x2, y1, y2)
    point_counter.update(iter_line(line))

print(sum(1 for (point, count) in point_counter.items() if count >= 2))