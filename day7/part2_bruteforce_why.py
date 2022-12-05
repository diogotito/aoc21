crabs = [*map(int, open('input.txt').readline().split(','))]

fuel_cost = lambda distance: (1 + distance) * distance // 2

for x in range(min(crabs), max(crabs) + 1):
	fuel_burnt = sum(fuel_cost(abs(x - crab)) for crab in crabs)
	print(f"{x}|{fuel_burnt}")