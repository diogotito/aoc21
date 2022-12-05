import time
start = time.process_time()

for i in range(10000):
	for instruction, amount in map(str.split, open("input.txt")):
		aim = depth = horizontal_pos = 0
		amount = int(amount)
		if instruction == "down":
			aim += amount
		elif instruction == "up":
			aim  -= amount
		elif instruction == "forward":
			horizontal_pos += amount
			depth += aim * amount

print(time.process_time() - start)  # 5.6
print(f"Submarine @ {horizontal_pos, depth}")
print("Answer is", horizontal_pos * depth)