from time import perf_counter


def energize(start, startD, maxX, maxY, neighbors):
    toEval = [(start, startD)]
    visited = set()

    while len(toEval) != 0:
        pos, d = toEval.pop(0)
        if (pos, d) in visited:
            continue

        visited.add((pos, d))
        
        newPos = tuple(p + o for p, o in zip(pos, d))
        if min(newPos) < 0 or newPos[0] >= maxX or newPos[1] >= maxY:
            continue

        for newD in neighbors[newPos][d]:
            toEval.append([newPos, newD])

    return set(v[0] for v in visited)


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    neighbors = {}
    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if l == '.':
                neighbors[(x, y)] = {(0, 1) : [(0, 1)], (0, -1) : [(0, -1)], (1, 0) : [(1, 0)], (-1, 0) : [(-1, 0)]}
            elif l == '|':
                neighbors[(x, y)] = {(0, 1) : [(0, 1)], (0, -1) : [(0, -1)], (1, 0) : [(0, 1), (0, -1)], (-1, 0) : [(0, 1), (0, -1)]}
            elif l == '-':
                neighbors[(x, y)] = {(0, 1) : [(1, 0), (-1, 0)], (0, -1) : [(1, 0), (-1, 0)], (1, 0) : [(1, 0)], (-1, 0) : [(-1, 0)]}
            elif l == '/':
                neighbors[(x, y)] = {(0, 1) : [(-1, 0)], (0, -1) : [(1, 0)], (1, 0) : [(0, -1)], (-1, 0) : [(0, 1)]}
            elif l == '\\':
                neighbors[(x, y)] = {(0, 1) : [(1, 0)], (0, -1) : [(-1, 0)], (1, 0) : [(0, 1)], (-1, 0) : [(0, -1)]}

    part1 = len(energize((-1, 0), (1, 0), len(lines[0]), len(lines), neighbors)) - 1

    part2 = 0
    for x in range(len(lines[0])):
        topSide = len(energize((x, -1), (0, 1), len(lines[0]), len(lines), neighbors)) - 1
        bottomSide = len(energize((x, len(lines)), (0, -1), len(lines[0]), len(lines), neighbors)) - 1
        part2 = max(part2, topSide, bottomSide)

    for y in range(len(lines)):
        leftSide = len(energize((-1, y), (1, 0), len(lines[0]), len(lines), neighbors)) - 1
        rightSide = len(energize((len(lines[0]), y), (-1, 0), len(lines[0]), len(lines), neighbors)) - 1
        part2 = max(part2, leftSide, rightSide)

    if verbose:
        print(f"\nPart 1:\nTiles energized: {part1}\n\nPart 2:\nMaximum tiles energized: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
