displays = [line.rstrip().split(' |' )[1].split() for line in open('input.txt')]
print(sum(len(digit) in (2, 3, 4, 7) for display in displays for digit in display))