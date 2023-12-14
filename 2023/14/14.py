from time import perf_counter
from collections import defaultdict


def roll(rocks, cubes, dir, maxVal):
    rocks = set(rocks)
    newRocks = set()

    positions = range(maxVal - 1, -1, -1) if sum(dir) > 0 else range(maxVal)

    for p1 in positions:
        nextPos = maxVal - 1 if sum(dir) > 0 else 0
        for p2 in positions:
            pos = (p1, p2) if dir[0] == 0 else (p2, p1)

            if pos in rocks:
                newRock = (p1, nextPos) if dir[0] == 0 else (nextPos, p1)
                if newRock in newRocks or newRock in cubes:
                    print("Error!")

                newRocks.add((p1, nextPos) if dir[0] == 0 else (nextPos, p1))
                nextPos -= sum(dir)

            if pos in cubes:
                nextPos = p2 - sum(dir)

    return tuple(newRocks)


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    cubes = set()
    rocks = set()

    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if l == '#':
                cubes.add((x, y))
            elif l == 'O':
                rocks.add((x, y))

    rocks = tuple(rocks)

    part1 = sum(len(lines) - p[1] for p in roll(rocks, cubes, (0, -1), len(lines)))

    states = defaultdict(lambda: [])
    goalIterations = 1000000000
    cycleFound = False
    iteration = 0

    while iteration < goalIterations:
        states[rocks].append(iteration)

        for dir in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            rocks = roll(rocks, cubes, dir, len(lines))

        iteration += 1

        if rocks in states and not cycleFound:
            cycleLen = iteration - states[rocks][-1]
            iteration += ((goalIterations - iteration) // cycleLen) * cycleLen
            cycleFound = True

    part2 = sum(len(lines) - p[1] for p in rocks)

    if verbose:
        print(f"\nPart 1:\nLoad on pillars: {part1}\n\nPart 2:\nLoad on pillars after 1,000,000,000 cycles: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
