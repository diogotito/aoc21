import itertools, collections, re

def my_range(a, b):
    step = (a < b) - (a > b)
    return range(a, b + step, step) if a != b else range(a, a + 1)

print(sum(1
    for (point, count) in collections.Counter(
        itertools.chain.from_iterable(
            (lambda x1, y1, x2, y2:
                (itertools.product if x1 == x2 or y1 == y2 else zip)(
                    my_range(x1, x2), my_range(y1, y2))
            )(*map(int, re.findall(r"\d+", line)))
            for line in open('input.txt'))
    ).items() if count >= 2))
