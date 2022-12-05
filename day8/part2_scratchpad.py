import collections
import itertools
import functools
import pprint

SEGMENTS = set("abcdefg")
A = ord("a")


def hash_pattern(pat):
    return sum(1 << ord(segment) - A for segment in pat)


class Display:
    def __init__(self, input_line):
        patterns, displays = input_line.split(" | ")
        self.patterns = [*map(set, patterns.split())]
        self.displays = [*map(hash_pattern, displays.split())]

    def deduce_wiring(self):
        # Indexa os padrões pelo seu comprimento
        by_len = collections.defaultdict(list)
        for pat in self.patterns:
            by_len[len(pat)].append(pat)

        # 1.
        pat_dict = {
            1: by_len[2].pop(),  # 1 tem 2 segmentos
            4: by_len[4].pop(),  # 4 tem 4 segmentos
            7: by_len[3].pop(),  # 7 tem 3 segmentos
            8: by_len[7].pop(),  # 8 tem 7 segmentos
        }

        # Há um segmento que é ligado em todos os padrões exceto no do 2
        [(almost_always_on, _)] = collections.Counter(
            itertools.chain.from_iterable(self.patterns)
        ).most_common(1)

        pat_dict[2] = by_len[5].pop(
            next(i for i, pat in enumerate(by_len[5]) if almost_always_on not in pat)
        )

        # o 9 tem o 4 e o 7
        pat_dict[9] = by_len[6].pop(
            next(
                i
                for i, pat in enumerate(by_len[6])
                if pat.issuperset(pat_dict[4]) and pat.issuperset(pat_dict[7])
            )
        )

        pat_dict[6] = by_len[6].pop(
            next(
                i
                for i, pat in enumerate(by_len[6])
                if (SEGMENTS - pat).pop() in pat_dict[1]  # "buraco" no 1
            )
        )

        pat_dict[0] = by_len[6].pop()

        pat_dict[3] = by_len[5].pop(
            next(i for i, pat in enumerate(by_len[5]) if len(pat - pat_dict[7]) == 2)
        )

        pat_dict[5] = by_len[5].pop()

        self.wiring = {hash_pattern(pat): n for n, pat in pat_dict.items()}
        return self

    def read_displays(self):
        return int("".join(str(self.wiring[n]) for n in self.displays))

    def read_displays_2(self):
        return functools.reduce(
            lambda acc, n: acc * 10 + self.wiring[n], self.displays, 0
        )

    def read_displays_3(self):
        return sum(10 ** (3 - i) * self.wiring[n] for i, n in enumerate(self.displays))


from time import perf_counter as clock

N_RUNS = 100
print(f"Running 10 x {N_RUNS} times...")
lines = open("input.txt").readlines()
for i in range(10):
    start = clock()
    for i in range(N_RUNS):
        sum(Display(line).deduce_wiring().read_displays_2() for line in lines)
    total_time = clock() - start
    print(f"  Total time: {total_time:.3f} seconds")

# Your puzzle answer was 989396.
