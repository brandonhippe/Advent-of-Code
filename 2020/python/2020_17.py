from itertools import product
from collections import defaultdict


def part1(data):
    """ 2020 Day 17 Part 1

    >>> part1(['.#.', '..#', '###'])
    112
    """

    cells = set()
    for y, line in enumerate(data):
        for x, l in enumerate(line):
            if l == '#':
                cells.add((x, y, 0))

    for _ in range(6):
        cells = iterate(cells)

    return len(cells)


def part2(data):
    """ 2020 Day 17 Part 2

    >>> part2(['.#.', '..#', '###'])
    848
    """

    cells = set()
    for y, line in enumerate(data):
        for x, l in enumerate(line):
            if l == '#':
                cells.add((x, y, 0, 0))

    for _ in range(6):
        cells = iterate(cells)

    return len(cells)


def iterate(cells):
    neighborCounts = defaultdict(lambda: 0)

    for pos in list(cells):
        for nOff in product(*[[n for n in range(-1, 2)] for _ in range(len(pos))]):
            if all(n == 0 for n in nOff):
                continue

            nPos = tuple(p + o for p, o in zip(pos, nOff))
            neighborCounts[nPos] += 1

    return set(p for p in neighborCounts.keys() if neighborCounts[p] == 3 or (p in cells and neighborCounts[p] == 2))


def main(verbose = False):
    from pathlib import Path
    import sys, re
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from Modules.timer import Timer
    year, day = re.findall('\d+', str(__file__))[-2:]
    
    with open(Path(__file__).parent.parent.parent / f"Inputs/{year}_{day}.txt", encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    with Timer() as p1_time:
        p1 = part1(data)

    if verbose:
        print(f"\nPart 1:\n3d cubes on after 6 cycles: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\n4d hypercubes on after 6 cycles: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)