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
        # Comecemos por agrupar e indexar os padrões pelo seu comprimento.
        by_len = collections.defaultdict(list)
        for pat in self.patterns:
            by_len[len(pat)].append(pat)

        # Encontrar os padrões do 1, 4, 7 e 8 é simples:
        pat_dict = {
            1: by_len[2].pop(),  # 1 tem 2 segmentos
            4: by_len[4].pop(),  # 4 tem 4 segmentos
            7: by_len[3].pop(),  # 7 tem 3 segmentos
            8: by_len[7].pop(),  # 8 tem 7 segmentos
        }

        # Vamos olhar para os três padrões com 6 segmentos: 9 6 0
        # o 9 tem de ter todos os segmentos do 4 e do 7
        pat_dict[9] = by_len[6].pop(
            next(
                i
                for i, pat in enumerate(by_len[6])
                if pat.issuperset(pat_dict[4] | pat_dict[7])
            )
        )

        # Dos digitos com 6 segmentos, o 6 é o que desliga um dos segmentos do 1
        pat_dict[6] = by_len[6].pop(
            next(
                i
                for i, pat in enumerate(by_len[6])
                if (SEGMENTS - pat).pop() in pat_dict[1]  # "buraco" no 1
            )
        )

        # Só sobra um digito de 6 segmentos: é o 0
        pat_dict[0] = by_len[6].pop()

        # Só faltam os padrões com 5 segmentos: 2 3 5
        # O segmento inferior direito é ligado em todos os padrões exceto no do 2
        [(almost_always_on, _)] = collections.Counter(
            itertools.chain.from_iterable(self.patterns)
        ).most_common(1)

        # O 2 é o único digito que desliga o segmento almost_always_on
        pat_dict[2] = by_len[5].pop(
            next(i for i, pat in enumerate(by_len[5]) if almost_always_on not in pat)
        )

        # Se aos segmentos do 3 desligarmos os do 7, ficamos com 2 segmentos ligados
        pat_dict[3] = by_len[5].pop(
            next(i for i, pat in enumerate(by_len[5]) if len(pat - pat_dict[7]) == 2)
        )

        # E temos o último algarismo: o 5
        pat_dict[5] = by_len[5].pop()

        self.wiring = {hash_pattern(pat): n for n, pat in pat_dict.items()}
        return self

    def read_4_displays(self):
        return (
            self.wiring[self.displays[0]] * 1000
            + self.wiring[self.displays[1]] * 100
            + self.wiring[self.displays[2]] * 10
            + self.wiring[self.displays[3]] * 1
        )


from time import perf_counter as clock

N_RUNS = 100
CORRECT_ANSWER = 989396
print(f"Running 10 x {N_RUNS} times...")
lines = open("input.txt").readlines()
for i in range(10):
    start = clock()
    for i in range(N_RUNS):
        result = sum(Display(line).deduce_wiring().read_4_displays() for line in lines)
        assert (
            result == CORRECT_ANSWER
        ), f"Expected {CORRECT_ANSWER}, got {result} (diff: {result - CORRECT_ANSWER})"
    total_time = clock() - start
    print(f"  Total time: {total_time:.3f} seconds")

# Your puzzle answer was 989396.
