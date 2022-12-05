parens = {"(": ")", "[": "]", "{": "}", "<": ">"}
error_score = {")": 3, "]": 57, "}": 1197, ">": 25137}


def score(line):
    stack = []
    for char in line:
        if char in "([{<":
            stack.append(char)
        else:
            open_paren = stack.pop()
            if parens[open_paren] != char:
                return error_score[char]
    return 0


print(sum(score(line.rstrip()) for line in open("input.txt")))
