import itertools

class Board:
    """A 5x5 board"""
    @staticmethod
    def from_lines(lines):
        b = Board()
        b.numbers = tuple(tuple(line) for line in lines)
        b.marked = [[False] * 5 for _ in range(5)]
        b.marked_T = [[False] * 5 for _ in range(5)]
        return b

    def __repr__(self):
        return repr((self.numbers, self.marked))

    def __iter__(self):
        board_indexes_it = itertools.product(range(5), range(5))
        board_numbers_it = itertools.chain.from_iterable(self.numbers)
        return zip(board_indexes_it, board_numbers_it)

    def mark_number(self, number):
        for (r, c), n in self:
            if n == number:
                self.marked[r][c] = self.marked_T[c][r] = True
                return self.is_winner()
        return False

    def is_winner(self):
        return any(map(all, self.marked)) or any(map(all, self.marked_T))

    def calculate_score(self):
        return sum(n for (r, c), n in self if not self.marked[r][c])


input_lines = map(str.rstrip, open('input.txt'))
numbers_drawn = map(int, next(input_lines).split(','))

boards = \
    [Board.from_lines(map(int, row.split()) for row in group)
    for not_empty, group in itertools.groupby(input_lines, bool) if not_empty]

for number in numbers_drawn:
    for board in boards[:]:                    # [:] para iterar numa shallow copy
        if board.mark_number(number):
            last_number, last_board = number, board
            boards.remove(board)               # para este .remove não estragar a iteração

print(last_number * last_board.calculate_score())
