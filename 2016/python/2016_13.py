import heapq


def part1(data, goal = (31, 39)):
    """ 2016 Day 13 Part 1

    >>> part1(['10'], (7, 4))
    11
    """

    return aStar(int(data[0]), goal)


def part2(data):
    """ 2016 Day 13 Part 1
    """

    return aStar(int(data[0]))


def manhatDist(p1, p2):
    return sum(abs(c1 - c2) for c1, c2 in zip(p1, p2))


def wall(pos, data):
    x, y = pos
    return len([c for c in bin(x*x + 3*x + 2*x*y + y + y*y + data)[2:] if c == '1']) % 2 == 1


def aStar(data, goal=None):
    openList = [[manhatDist((1, 1), goal) if goal is not None else 0, 0, (1, 1)]]
    visited = {}
    under50 = set()

    while len(openList) != 0:
        currF, currG, currPos = heapq.heappop(openList)

        if currG <= 50:
            under50.add(currPos)

        if goal is not None and currPos == goal:
            return currG

        for n in [tuple(p + o for p, o in zip(currPos, offset)) for offset in [[0, 1], [0, -1], [1, 0], [-1, 0]]]:
            if min(n) < 0 or wall(n, data) or (goal is None and manhatDist(n, (1, 1)) > 50):
                continue

            nH, nG = manhatDist(n, goal) if goal is not None else 0, currG + 1
            nF = nH + nG

            if n in visited and visited[n] <= nF:
                continue

            continuing = False
            for f, _, pos in openList:
                if pos == n and f <= nF:
                    continuing = True
                    break

            if continuing:
                continue

            heapq.heappush(openList, [nF, nG, n])

        visited[currPos] = currF

    return len(under50)


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
        print(f"\nPart 1:\nShortest path to (31, 39): {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nPositions reached in at most 50 steps: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)