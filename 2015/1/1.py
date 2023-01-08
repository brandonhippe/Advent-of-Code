import time
from collections import defaultdict
import os

def findFloor(data):
    counts = defaultdict(lambda: 0)
    for d in data:
        counts[d] += 1

    return counts['('] - counts[')']

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        data = f.readline().strip('\n')

    part1 = findFloor(data)

    for n in range(1, len(data) + 1):
        if findFloor(data[:n]) < 0:
            break

    part2 = n

    if verbose:
        print(f"\nPart 1:\nFloor Santa ends up on: {part1}\n\nPart 2:\nPosition of first character that sends Santa to the basement: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
