import collections
import pprint
import re
import sys

def my_range(a, b):
    """range(), mas fechado e se a > b vai de cima para baixo
    >>> my_range(1, 10)
    range(1, 11)
    >>> my_range(10, 1)
    range(10, 0, -1)
    >>> my_range(10, 10)
    range(10, 11)
    >>> my_range(10, 11)
    range(10, 12)
    >>> my_range(11, 10)
    range(11, 9, -1)
    """
    step = (a < b) - (a > b)
    return range(a, b + step, step) if a != b else range(a, a + 1)

import doctest
doctest.testmod()
sys.exit(0)

def iter_line(x1, y1, x2, y2):
    if x1 == x2:
        yield from iter_horizontal(x1, y1, y2)

def iter_horizontal(x, y1, y2):
    for y in range(min(y1, y2), max(y1, y2) + 1, (y1 > y2) - (y1 < y2)):
        yield (x, y)



for line in open('input.txt'):
    digits = re.findall(r"\d+", line)
    [x1, x2, y1, y2] = [int(n) for n in digits]
    line = Line(x1, x2, y1, y2)
    print(list(iter_line(line)))
