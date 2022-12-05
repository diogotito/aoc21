import collections
import pprint

SEGMENTS = set("abcdefg")


class Display:
    def __init__(self, input_line):
        patterns, displays = input_line.split(" | ")
        self.patterns = [*map(set, patterns.split())]
        self.displays = [*map(set, displays.split())]

    def solve(self):
        """O meu processo para resolver isto:
        1. Encontrar os padrões com comprimento 2, 3, 4, 7 e atribuí-los aos
           números 1, 7, 4 e 8, respetivamente
        2. Nos padrões com comprimento 6 (i.e. os que têm um "buraco")
            2.1. Atribuir 6 àquele que tiver o buraco num dos segmentos do 1
            2.2. Atribuir 0 àquele que tiver o buraco num dos segmentos do 4
            2.3. Atribuir 9 ao que ficar
        3. Restam os padrões com comprimento 5 (i.e. os que têm dois "buracos")
            3.1. Atribuir 5 àquele cujos buracos forem o do 6 e o do 9
            3.2. Atribuir 2 àquele em que um dos buracos é o do 9
            3.3. Atribuir 3 ao que ficar
        """

        # Indexa os padrões pelo seu comprimento
        by_len = collections.defaultdict(list)
        for pat in self.patterns:
            by_len[len(pat)].append(pat)

        # 1.
        self.wiring = {
            1: by_len[2].pop(),  # 1 tem 2 segmentos
            4: by_len[4].pop(),  # 4 tem 4 segmentos
            7: by_len[3].pop(),  # 7 tem 3 segmentos
            8: by_len[7].pop(),  # 8 tem 7 segmentos
        }

        # 2.
        # Vamos olhar para os segmentos apagados dos padrões com comprimento 6
        def len_6_holes():
            for i, pattern in enumerate(by_len[6]):
                yield i, (SEGMENTS - pattern).pop()

        i, hole_6 = next(
            (i, hole) for i, hole in len_6_holes() if hole in self.wiring[1]
        )
        self.wiring[6] = by_len[6].pop(i)

        self.wiring[0] = by_len[6].pop(
            next(
                i
                for i, hole in len_6_holes()
                if hole in self.wiring[4] and not hole in self.wiring[7]
            )
        )  # and not hole in self.wiring[7]

        self.wiring[9] = by_len[6].pop()
        hole_9 = (SEGMENTS - self.wiring[9]).pop()

        # 3.
        # Vamos olhar para os segmentos apagados dos padrões com comprimento 5
        def len_5_holes():
            for i, pattern in enumerate(by_len[5]):
                yield i, SEGMENTS - pattern

        self.wiring[5] = by_len[5].pop(
            next(i for i, holes in len_5_holes() if holes == {hole_6, hole_9})
        )

        self.wiring[2] = by_len[5].pop(
            next(i for i, holes in len_5_holes() if hole_9 in holes)
        )

        print(*by_len[5])

        print()
        pprint.pprint(self.wiring)


displays = [Display(line) for line in open("input.txt")]

displays[0].solve()
