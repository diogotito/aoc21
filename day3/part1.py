from collections import Counter

lines = map(str.rstrip, open('input.txt'))
cols = zip(*lines)
bitcount = [Counter(col).most_common() for col in cols]

epsilon_binary = ''.join(bit for (bit, _), _ in bitcount)
gamma_binary   = ''.join(bit for _, (bit, _) in bitcount)

epsilon = int(epsilon_binary, 2)
gamma = int(gamma_binary, 2)

print(epsilon * gamma)