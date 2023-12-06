from time import perf_counter
import re
import numpy as np
import math


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    times = [int(n) for n in re.findall('\d+', lines[0])]
    distances = [int(n) for n in re.findall('\d+', lines[1])]

    part1 = 1

    for t, d in zip(times, distances):
        winCounts = 0

        for s in range(t):
            winCounts += (t - s) * s > d

        part1 *= winCounts

    t = int(lines[0].replace(' ', '').split(':')[1])
    d = int(lines[1].replace(' ', '').split(':')[1])

    roots = np.roots([1, -t, d])
    part2 = math.floor(max(roots)) - math.ceil(min(roots)) + 1

    if verbose:
        print(f"\nPart 1:\n{part1}\n\nPart 2:\n{part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
