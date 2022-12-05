import collections

counter = collections.Counter(
    int(fish) for fish in open('input.txt').readline().split(','))

school = [0] + [count for key, count in sorted(counter.items())] + [0, 0, 0]
print("  Start:", sum(school))

for day in range(256):
    spawns = school[0]
    school[0] = school[1]
    school[1] = school[2]
    school[2] = school[3]
    school[3] = school[4]
    school[4] = school[5]
    school[5] = school[6]
    school[6] = school[7] + spawns
    school[7] = school[8]
    school[8] = spawns
    print(f"Day {day + 1:>3}: {sum(school)}")

print(sum(school))
