import time
from itertools import product
from collections import defaultdict

def iterate(cells):
    neighborCounts = defaultdict(lambda: 0)

    for pos in list(cells):
        for nOff in product(*[[n for n in range(-1, 2)] for _ in range(len(pos))]):
            if all(n == 0 for n in nOff):
                continue

            nPos = tuple(p + o for p, o in zip(pos, nOff))
            neighborCounts[nPos] += 1

    return set(p for p in neighborCounts.keys() if neighborCounts[p] == 3 or (p in cells and neighborCounts[p] == 2))

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    cellsP1 = set()
    cellsP2 = set()
    for y, line in enumerate(data):
        for x, l in enumerate(line):
            if l == '#':
                cellsP1.add((x, y, 0))
                cellsP2.add((x, y, 0, 0))

    for _ in range(6):
        cellsP1 = iterate(cellsP1)
        cellsP2 = iterate(cellsP2)

    if verbose:
        print(f"\nPart 1:\n3d cubes on after 6 cylces: {len(cellsP1)}\n\nPart 2:\n4d hypercubes on after 6 cycles: {len(cellsP2)}")

    return [len(cellsP1), len(cellsP2)]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
