from collections import Counter
from pprint import pprint
lines = [*map(str.rstrip, open('input.txt'))]
num_cols = len(lines[0])

# ===== search for oxygen generator rating =====

oxygen_lines = lines.copy()
oxygen_cols = [*zip(*oxygen_lines)]

for col_i in range(num_cols):
	bit_count = Counter(oxygen_cols[col_i]).most_common()
	if len(bit_count) == 2:
		most_common_bit = bit_count[0][0] if bit_count[0][1] != bit_count[1][1] else '1'
	else:
		most_common_bit = bit_count[0][0]
	print(f"{str(bit_count):-<30} {most_common_bit=}")

	oxygen_lines = [l for l in oxygen_lines if l[col_i] == most_common_bit]
	if len(oxygen_lines) == 1:
		break
	if not oxygen_lines:
		raise "This wasn't supposed to happen"
	oxygen_cols = [*zip(*oxygen_lines)]

print(oxygen_lines)

# ===== search for CO2 scrubber rating =====

co2_lines = lines.copy()
co2_cols = [*zip(*co2_lines)]

for col_i in range(num_cols):
	bit_count = Counter(co2_cols[col_i]).most_common()
	if len(bit_count) == 2:
		least_common_bit = bit_count[1][0] if bit_count[0][1] != bit_count[1][1] else '0'
	else:
		raise "I don't know what to do here"
	print(f"{str(bit_count):.<30} {least_common_bit=}")

	co2_lines = [l for l in co2_lines if l[col_i] == least_common_bit]
	if len(co2_lines) == 1:
		break
	co2_cols = [*zip(*co2_lines)]

print(co2_lines)

oxygen_rating = int(oxygen_lines[0], 2)
co2_rating = int(co2_lines[0], 2)
print(oxygen_rating * co2_rating)