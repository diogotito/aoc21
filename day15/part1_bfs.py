import collections

cave = [list(map(int, line.rstrip())) for line in open("input_S.txt")]
SIZE = len(cave)
DEST = (SIZE - 1,) * 2


# pprint.pprint(cave, width=310)

def neighbours(pos):
    x, y = pos
    yield x, y + 1
    yield x + 1, y
    yield x - 1, y
    yield x, y - 1


def in_grid(pos):
    x, y = pos
    return (0 <= x < SIZE) and (0 <= y < SIZE)


def risk_at_position(pos):
    x, y = pos
    return cave[y][x]


def manhattan_distance(pos):
    x, y = pos
    return (SIZE - x) + (SIZE - y)


def heuristic(pos):
    """lower == probably better"""
    return 5 * risk_at_position(pos) + 2 * manhattan_distance(pos)


count = 0
min_risk = 9 * SIZE * SIZE
cuts = 0


def visualize_path(entered_cells):
    import os
    os.system("color")
    COLORS = [30, 37, 36, 35, 34, 33, 32, 32, 31, 31]
    for y in range(SIZE):
        for x in range(SIZE):
            risk = risk_at_position((x, y))
            trail = (x, y) in entered_cells
            print(f'\033[{7 if trail else 0}m\033[{COLORS[trail and risk]}m{risk}', end='\033[0m')
        print()


def breadth_first_search():
    current_position = (0, 0)
    trail = {(current_position, 0)}
    visited_positions = set()
    search_queue = collections.deque(filter(in_grid, neighbours(current_position)))

    while search_queue:
        current_position = search_queue.popleft()

        trail.add((current_position, risk_at_position(current_position)))
        visited_positions.add(current_position)

        search_queue.extend(p for p in neighbours(current_position) if in_grid(p) and p not in visited_positions)


breadth_first_search()

# 1667: too high
# 2549: too high
# 912:  too high
# 891:  incorrect
# 885:  incorrect
# 883:  incorrect
