import collections, itertools, re

def my_range(a, b):
    step = (a < b) - (a > b)
    return range(a, b + step, step) if a != b else range(a, a + 1)

def iter_line(x1, y1, x2, y2):
    f = itertools.product if x1 == x2 or y1 == y2 else zip
    return f(my_range(x1, x2), my_range(y1, y2))

# ------------------------------------------------------------------------

point_counter = collections.Counter()

for line_coords in map(re.compile(r"\d+").findall, open('input.txt')):
    point_counter.update(iter_line(*map(int, line_coords)))

print(sum(1 for (point, count) in point_counter.items() if count >= 2))
