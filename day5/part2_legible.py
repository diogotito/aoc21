import collections
import re
import pprint

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


def iter_line(x1, y1, x2, y2):
    """Produz pares (x, y) para todos os pontos numa linha que vai
    de (x1, y1) a (x2, y2)
    """

    # Horizontal line
    if x1 == x2:
        for y in my_range(y1, y2):
            yield (x1, y)

    # Vertical line
    elif y1 == y2:
        for x in my_range(x1, x2):
            yield (x, y1)

    # Diagonal lines
    else:
        for x, y in zip(my_range(x1, x2), my_range(y1, y2)):
            yield (x, y)


point_counter = collections.Counter()


for line in open('input.txt'):
    digits = re.findall(r"\d+", line)
    [x1, x2, y1, y2] = [int(n) for n in digits]
    point_counter.update(iter_line(x1, x2, y1, y2))

print(sum(1 for (point, count) in point_counter.items() if count >= 2))
