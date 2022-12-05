import collections

counter = collections.Counter(
    int(fish) for fish in open('input.txt').readline().split(','))

school = collections.deque(
    [0, counter[1], counter[2], counter[3], counter[4], counter[5], 0, 0, 0])

# print("  Start:", sum(school))

for day in range(256):
    spawns = school.popleft()
    school.append(spawns)
    school[6] += spawns
    # print(f"Day {day + 1:>3}: {sum(school)}")

print(sum(school))
