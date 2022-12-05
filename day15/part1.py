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


def gonna_get_stuck(pos, next_pos, trail):
    """This should cut down tons of expensive useless search branches"""
    global cuts
    x1, y1 = pos
    x2, y2 = next_pos

    # If we reached a side wall of the cave we shouldn't turn backwards!
    if x1 in (0, SIZE - 1) and y2 < y1:
        cuts += 1
        return True

    # If we reached the front or back wall of the cave we shouldn't turn left!
    if y1 in (0, SIZE - 1) and x2 < x1:
        cuts += 1
        return True

    # We shouldn't go down if the position on the left is trailed

    # Ok to go!
    return False


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


def walk(position, entered_cells, depth=0, cur_risk=0):
    global count, min_risk
    count += 1

    # Periodic debugging
    if count % 1000000 == 0:
        # Steps walked globally and in this branch, recursion depth, furthest position reached
        print(count, len(entered_cells), sorted(entered_cells, key=manhattan_distance)[0], f'{min_risk=}')
        visualize_path(entered_cells)

    # Bail out if we walked too much
    if depth > SIZE * 9:
        return

    # Bail out if this branch is revealing to be too much risky
    if cur_risk >= 885:
        return

    if position == DEST:
        # We have arrived!!
        risk = sum(map(risk_at_position, entered_cells))
        min_risk = min(min_risk, risk)
        print(f"length: {len(entered_cells):>3d},  risk: {risk:>4d}  ({min_risk:>4d})   | {count} {cuts}")
        visualize_path(entered_cells)
        return

    for adj_pos in sorted(filter(in_grid, neighbours(position)), key=heuristic):
        # for adj_pos in neighbours(position):
        if adj_pos not in entered_cells and not gonna_get_stuck(position, adj_pos, entered_cells):
            walk(adj_pos, entered_cells + collections.deque([adj_pos]), depth + 1, cur_risk + risk_at_position(adj_pos))


walk((0, 0), collections.deque())

# 1667: too high
# 2549: too high
# 912:  too high
# 891:  incorrect
# 885:  incorrect
# 883:  incorrect
