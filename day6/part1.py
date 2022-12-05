import collections

school = collections.Counter(
    int(fish) for fish in open('input.txt').readline().split(','))

print("  Start:", school.total())


for day in range(256):
    school = collections.Counter({
        8: school[0],
        7: school[8],
        6: school[7] + school[0],
        5: school[6],
        4: school[5],
        3: school[4],
        2: school[3],
        1: school[2],
        0: school[1],
    })
    print(f"Day {day + 1:>3}: {school.total()}")
