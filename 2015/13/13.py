import time
import re
from itertools import permutations

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('.\n') for line in f.readlines()]

    for i, line in enumerate(lines):
        line = re.sub('lose ', 'gain -', line).split(' ')
        lines[i] = [line[0], int(line[3]), line[-1]]

    data = {line[0]: {} for line in lines}
    for line in lines:
        data[line[0]][line[-1]] = line[1]

    best = float('-inf')
    for p in permutations(data.keys()):
        total = 0
        for i, name in enumerate(p):
            total += data[name][p[(i + 1) % len(p)]]
            total += data[name][p[(i - 1) % len(p)]]

        if total > best:
            best = total

    print(f"\nPart 1:\nChange in happiness for optimal seating arrangement: {best}")

    data['Me'] = {k: 0 for k in data.keys()}
    for k in data.keys():
        data[k]['Me'] = 0

    best = float('-inf')
    for p in permutations(data.keys()):
        total = 0
        for i, name in enumerate(p):
            total += data[name][p[(i + 1) % len(p)]]
            total += data[name][p[(i - 1) % len(p)]]

        if total > best:
            best = total

    print(f"\nPart 2:\nChange in happiness for optimal seating arrangement: {best}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
