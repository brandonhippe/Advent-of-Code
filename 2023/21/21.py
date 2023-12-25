from time import perf_counter


def triangle(n):
    return n * (n + 1) // 2


def manhatArea(base):    
    return 1 + (4 * triangle(base // 2))


def bfs(pos, area, maxSteps = float('inf')):
    visited = {}
    openList = {pos}
    steps = 0
    added = 1

    while len(visited) != len(area) and added and steps <= maxSteps:
        newOpenList = set()
        added = 0
        for pos in openList:
            visited[pos] = steps

            for offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                newPos = tuple(p + o for p, o in zip(pos, offset))
                if newPos in area and newPos not in visited:
                    newOpenList.add(newPos)
                    added += 1

        openList = newOpenList
        steps += 1

    return visited


def fillmap(startStep, frame, steps, pos, area):
    positions = {pos}
    for i in range(steps):
        nPositions = set()
        for pos in positions:
            for offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                areaIndex = tuple((p + o) % frame for p, o in zip(pos, offset))
                nPos = tuple(p + o for p, o in zip(pos, offset))

                if areaIndex in area:
                    nPositions.add(nPos)

        positions = nPositions

        if i % frame == startStep - 1:
            yield len(positions)

    return


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    area = set()

    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if l == '#':
                continue

            if l == 'S':
                pos = (x, y)

            area.add((x, y))
    
    part1 = len([v for v in bfs(pos, area, 64).values() if 0 <= v <= 64 and v % 2 == 0])

    dim = len(lines)
    a = []
    for res in fillmap(dim // 2, dim, dim * 2 + dim // 2 + 1, pos, area):
        a.append(res)

    i = dim
    s = a[1] - a[0]
    r = a[2] - a[1]
    d = r - s
    part2 = a[1]

    while i != 26501365 - dim // 2:
        i += dim
        part2 += r
        r += d

    if verbose:
        print(f"\nPart 1:\nPlots Reached: {part1}\n\nPart 2:\nPlots Reached: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
