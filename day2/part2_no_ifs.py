def down(amount):
	global aim
	aim += amount


def up(amount):
	global aim
	aim -= amount


def forward(amount):
	global horizontal_pos, depth
	horizontal_pos += amount
	depth += aim * amount

d = {'down': down, 'up': up, 'forward': forward}

import time
start = time.process_time()

for i in range(10000):
	aim = depth = horizontal_pos = 0
	for instruction, amount in map(str.split, open("input.txt")):
		globals()[instruction](int(amount))

print(time.process_time() - start)  # 5.8 com globals(), 5.5 com d
print(f"Submarine @ {horizontal_pos, depth}")
print("Answer is", horizontal_pos * depth)