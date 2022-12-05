import time

start_time = time.time()
input_file = open('inputFinal.txt', 'r')

num_lines_half = sum(1 for line in input_file) / 2
input_file.seek(0)
line_size = len(input_file.readline())-1
input_file.seek(0)
res = [0] * line_size

solution_dicts = [
    {0: [], 1: []} for x in range(line_size)
]

for line in input_file:
    line_no_n = line.rstrip()
    for i, char in enumerate(line):
        if char == '0':
            solution_dicts[i][0].append(line_no_n)
        elif char == '1':
            solution_dicts[i][1].append(line_no_n)

#intialize set
if len(solution_dicts[0][1]) > len(solution_dicts[0][0]):
    set_res_oxi = set(solution_dicts[0][1])
    set_res_doxi = set(solution_dicts[0][0])

for i, dict in enumerate(solution_dicts):
    if i == 0:
        continue

    set_0_oxi = set_res_oxi.intersection(dict[0])
    set_1_oxi = set_res_oxi.intersection(dict[1])

    set_0_doxi = set_res_doxi.intersection(dict[0])
    set_1_doxi = set_res_doxi.intersection(dict[1])

    if len(set_res_oxi) == 1:
        continue

    if len(set_1_oxi) >= len(set_0_oxi):
        set_res_oxi = set_1_oxi
    else:
        set_res_oxi = set_0_oxi

    if len(set_res_doxi) == 1:
        continue

    if len(set_1_doxi) >= len(set_0_doxi):
        set_res_doxi = set_0_doxi
    else:
        set_res_doxi = set_1_doxi

print(int(set_res_oxi.pop(), 2) * int(set_res_doxi.pop(), 2))
print( time.time()-start_time)