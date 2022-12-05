import functools
import statistics
import pprint

parens = {"(": ")", "[": "]", "{": "}", "<": ">"}
autocompletion_score = {"(": 1, "[": 2, "{": 3, "<": 4}


def score(line):
    stack = []
    for char in line:
        if char in "([{<":
            stack.append(char)
        else:
            open_paren = stack.pop()
            if parens[open_paren] != char:
                return 0
    return functools.reduce(
        lambda acc, par: acc * 5 + autocompletion_score[par], reversed(stack), 0
    )


completion_scores = [score(line.rstrip()) for line in open("input.txt")]
completion_scores = [score for score in completion_scores if score > 0]
print(statistics.median(completion_scores))
