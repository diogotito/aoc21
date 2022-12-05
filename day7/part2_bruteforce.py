crabs = [*map(int, open('input.txt').readline().split(','))]

fuel_cost = lambda distance: (1 + distance) * distance // 2

print(min(
	sum(fuel_cost(abs(crab - x)) for crab in crabs)
	for x in range(min(crabs), max(crabs) + 1)))     # Try every x position
