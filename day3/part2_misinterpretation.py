from collections import Counter
from pprint import pprint

lines = [*map(str.rstrip, open('input.txt'))]
cols = [*zip(*lines)]
most_common_bits = [Counter(col).most_common()[0][0] for col in cols]
pprint(most_common_bits)
print(len(lines))


# search for oxygen generator rating

oxygen_lines = lines.copy()
for col_i, most_common in enumerate(most_common_bits):
	oxygen_lines = [line for line in oxygen_lines if line[col_i] == most_common]
	pprint((col_i, len(oxygen_lines), most_common, oxygen_lines))
	if len(oxygen_lines) == 1:
		break


# search for CO2 scrubber rating

co2_lines = lines.copy()
for col_i, most_common in enumerate(most_common_bits):
	co2_lines = [line for line in co2_lines if line[col_i] != most_common]
	pprint((col_i, len(co2_lines), most_common, co2_lines))
	if len(co2_lines) == 1:
		break


oxygen_rating = int(oxygen_lines[0], 2)
co2_rating = int(co2_lines[0], 2)

print(oxygen_rating * co2_rating)