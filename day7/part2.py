from math import floor

# Soma dos termos de uma progressão aritmética
fuel_cost = lambda distance: (1 + distance) * distance // 2

crabs = [*map(int, open('input.txt').readline().split(','))]

# não faço a mínima porquê mas isto dá-me a resposta certa
closest = floor(sum(crabs) / len(crabs))  # round() não acerta

print(sum(fuel_cost(abs(closest - crab)) for crab in crabs))
