def part1(data, steps = 64):
    """ 2023 Day 21 Part 1

    >>> part1(['...........', '.....###.#.', '.###.##..#.', '..#.#...#..', '....#.#....', '.##..S####.', '.##..#...#.', '.......##..', '.##.#.####.', '.##..##.##.', '...........'], 6)
    16
    """

    area = set()

    for y, line in enumerate(data):
        for x, l in enumerate(line):
            if l == '#':
                continue

            if l == 'S':
                pos = (x, y)

            area.add((x, y))
    
    return len([v for v in bfs(pos, area, len(data), steps).values() if 0 <= v <= steps and v % 2 == steps % 2])


def part2(data):
    """ 2023 Day 21 Part 2
    """

    area = set()

    for y, line in enumerate(data):
        for x, l in enumerate(line):
            if l == '#':
                continue

            if l == 'S':
                pos = (x, y)

            area.add((x, y))

    dim = len(data)
    dists = bfs(pos, area, dim, pos[0] + dim * 4)
    counts = []
    for i in range(3):
        steps = pos[0] + dim * 2 * i
        counts.append(len([v for v in dists.values() if 0 <= v <= steps and v % 2 == steps % 2]))

    a = (counts[2] - 2 * counts[1] + counts[0]) // 2
    b = counts[1] - counts[0] - a
    c = counts[0]
    n = 26501365 // (2 * dim)

    return a * n ** 2 + b * n + c


def bfs(pos, area, dim, maxSteps = float('inf')):
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
                if (newPos[0] % dim, newPos[1] % dim) in area and newPos not in visited:
                    newOpenList.add(newPos)
                    added += 1

        openList = newOpenList
        steps += 1

    return visited


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
        print(f"\nPart 1:\nPlots Reached: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nPlots Reached: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)