import itertools


def main():
    parsed_words = [
        [words.split() for words in line.split("|")]
        for line in lines  # replaced open('...').readlines() with lines
    ]
    sum = 0
    for line_index in range(len(parsed_words)):
        decrypted_nums = [set()] * 10
        chars_to_decrypted_nums = {}

        # decrypt initial numbers
        for word_index in range(len(parsed_words[0][0])):
            word = parsed_words[line_index][0][word_index]
            word_set = set([char for char in word])

            # decrypt 1
            if len(word) == 2:
                decrypted_nums[1] = word_set
                chars_to_decrypted_nums[frozenset(word_set)] = 1

            # decrypt 7
            elif len(word) == 3:
                decrypted_nums[7] = word_set
                chars_to_decrypted_nums[frozenset(word_set)] = 7

            # decrypt 4
            elif len(word) == 4:
                decrypted_nums[4] = word_set
                chars_to_decrypted_nums[frozenset(word_set)] = 4

            # decrypt 8
            elif len(word) == 7:
                decrypted_nums[8] = word_set
                chars_to_decrypted_nums[frozenset(word_set)] = 8

        # decrypt 9, 6, 0
        for word_index in range(len(parsed_words[0][0])):
            word = parsed_words[line_index][0][word_index]
            word_set = set([char for char in word])

            if len(word) == 6:
                # decrypt 9
                if decrypted_nums[4].issubset(word_set):
                    decrypted_nums[9] = word_set
                    chars_to_decrypted_nums[frozenset(word_set)] = 9

                # decrypt 0
                elif decrypted_nums[1].issubset(word_set):
                    decrypted_nums[0] = word_set
                    chars_to_decrypted_nums[frozenset(word_set)] = 0

                # decrypt 6
                else:
                    decrypted_nums[6] = word_set
                    chars_to_decrypted_nums[frozenset(word_set)] = 6

        # decrypt 2, 3, 5
        for word_index in range(len(parsed_words[0][0])):
            word = parsed_words[line_index][0][word_index]
            word_set = set([char for char in word])

            if len(word) == 5:
                # decrypt 3
                if decrypted_nums[1].issubset(word_set):
                    decrypted_nums[3] = word_set
                    chars_to_decrypted_nums[frozenset(word_set)] = 3

                # decrypt 5
                elif len(word_set.intersection(decrypted_nums[6])) == 5:
                    decrypted_nums[5] = word_set
                    chars_to_decrypted_nums[frozenset(word_set)] = 5

                # decrypt 2
                else:
                    decrypted_nums[2] = word_set
                    chars_to_decrypted_nums[frozenset(word_set)] = 2

        # calculate the output
        nums = []
        for word_index in range(len(parsed_words[0][1])):
            word = parsed_words[line_index][1][word_index]
            word_set = set([char for char in word])
            num = chars_to_decrypted_nums[frozenset(word_set)]
            nums.append(str(num))
        line_res = int("".join(nums))
        sum += line_res

    return sum


#
# MINI BENCHMARK
#
from time import perf_counter as clock

INPUT_FILE = "input.txt"
N_RUNS = 100
CORRECT_ANSWER = 989396

if __name__ == "__main__":
    print(f"Running 10 x {N_RUNS} times...")
    lines = open(INPUT_FILE).readlines()

    for i in range(10):
        start = clock()
        for _ in range(N_RUNS):
            result = main()
            assert (
                result == CORRECT_ANSWER
            ), f"Expected {CORRECT_ANSWER}, got {result} (diff: {result - CORRECT_ANSWER})"
        total_time = clock() - start
        print(f"{i+1:>4d}. Avg. per run: {1000 * total_time / N_RUNS:.3f} ms")
