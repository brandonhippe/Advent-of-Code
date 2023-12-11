from time import perf_counter
from itertools import combinations


def galaxyDist(p1, p2, expandMult, emptyX, emptyY):
    betweenX = []
    betweenY = []

    for x in emptyX:
        if max(p1[0], p2[0]) < x:
            break

        if min(p1[0], p2[0]) < x:
            betweenX.append(x)

    for y in emptyY:
        if max(p1[1], p2[1]) < y:
            break

        if min(p1[1], p2[1]) < y:
            betweenY.append(y)

    return sum(abs(c1 - c2) for c1, c2 in zip(p1, p2)) + (expandMult - 1) * (len(betweenX) + len(betweenY))


def manhatDist(p1, p2):
    return sum(abs(c1 - c2) for c1, c2 in zip(p1, p2))


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    xVals = set(range(len(lines[0])))
    yVals = set(range(len(lines)))
    galaxies = []
    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if l == '#':
                if x in xVals:
                    xVals.remove(x)

                if y in yVals:
                    yVals.remove(y)

                galaxies.append((x, y))

    emptyX = sorted(xVals)
    emptyY = sorted(yVals)

    part1 = sum(galaxyDist(g1, g2, 2, emptyX, emptyY) for g1, g2 in combinations(galaxies, 2))
    part2 = sum(galaxyDist(g1, g2, 1_000_000, emptyX, emptyY) for g1, g2 in combinations(galaxies, 2))

    if verbose:
        print(f"\nPart 1:\n{part1}\n\nPart 2:\n{part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
