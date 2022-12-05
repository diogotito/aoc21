import itertools
import collections
import re

def my_range(a, b):
    """range(), mas fechado e se a > b vai de cima para baixo"""
    step = (a < b) - (a > b)
    return range(a, b + step, step) if a != b else range(a, a + 1)


def iter_line(x1, y1, x2, y2):
    if x1 == x2 or y1 == y2:
        # Horizontal and vertical lines
        for x, y in itertools.product(my_range(x1, x2), my_range(y1, y2)):
            yield (x, y)
    else:
        # Diagonal lines
        for x, y in zip(my_range(x1, x2), my_range(y1, y2)):
            yield (x, y)


point_counter = collections.Counter()


# for line in open('input.txt'):
#     digits = re.findall(r"\d+", line)
#     [x1, y1, x2, y2] = [int(n) for n in digits]
#     line = Line(x1, y1, x2, y2)
#     point_counter.update(iter_line(line))

print(sum(1
    for (point, count) in collections.Counter(
        itertools.chain.from_iterable(
            iter_line(*map(int, re.findall(r"\d+", line)))
            for line in open('input.txt'))
    ).items() if count >= 2))
