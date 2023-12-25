from time import perf_counter
from collections import deque
import heapq


DIRS = {'<': (-1, 0), '>': (1, 0), 'v': (0, 1), '^': (0, -1)}


def bfs(start, end, nodes):
    openList = deque()
    openList.append((0, start, {start}))

    longest = -1

    while len(openList) != 0:
        q, pos, currPath = openList.popleft()

        if pos == end:
            longest = max(longest, q)
            continue

        for nPos, pLen in nodes[pos].items():
            if nPos not in currPath:
                openList.append((q + pLen, nPos, currPath.union({nPos})))

    return longest


def manhatDist(p1, p2):
    return sum(abs(c1 - c2) for c1, c2 in zip(p1, p2))


def aStar(start, end, nodes):
    openList = [(0, 0, start, {start})]
    openDict = {start: 0}

    closedDict = {}

    while len(openDict) != 0:
        f, g, pos, path = heapq.heappop(openList)
        if pos == end:
            return -g
        
        if pos in openDict:
            del(openDict[pos])

        for nPos, pLen in nodes[pos].items():
            nG = g - pLen
            nF = nG - manhatDist(nPos, end)

            if nPos in path or (nPos in openDict and openDict[nPos] <= nF) or (nPos in closedDict and closedDict[nPos] <= nF):
                continue

            heapq.heappush(openList, (nF, nG, nPos, path.union({nPos})))
            openDict[nPos] = nF

        closedDict[nPos] = f

    return -1


def determineNeighbors(nodes, paths, slopes, part):
    for pos in nodes.keys():
        visited = set()
        openList = deque()
        openList.append((0, pos))

        while len(openList) != 0:
            pathLen, currPos = openList.popleft()

            if currPos in visited:
                continue

            if currPos != pos and currPos in nodes:
                nodes[pos][currPos] = pathLen
                continue

            visited.add(currPos)

            if part == 1 and currPos in slopes:
                neighbors = [DIRS[slopes[currPos]]]
            else:
                neighbors = DIRS.values()

            for offset in neighbors:
                newPos = tuple(p + o for p, o in zip(currPos, offset))
                if newPos not in visited and (newPos in slopes or newPos in paths):
                    openList.append((pathLen + 1, newPos))


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    slopes = {}
    paths = set()
    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if l == '#':
                continue

            if l == '.':
                paths.add((x, y))
                if y == 0:
                    start = (x, y)
                if y == len(lines) - 1:
                    end = (x, y)
            else:
                slopes[(x, y)] = l

    nodesP1 = {start: {}, end: {}}
    nodesP2 = {start: {}, end: {}}

    for pos in list(slopes.keys()) + list(paths):
        neighbors = []
        for offset in DIRS.values():
            nPos = tuple(p + o for p, o in zip(pos, offset))

            if nPos in slopes or nPos in paths:
                neighbors.append(nPos)

        if len(neighbors) > 2:
            if pos in paths:
                nodesP1[pos] = {}

            nodesP2[pos] = {}

    determineNeighbors(nodesP1, paths, slopes, 1)
    determineNeighbors(nodesP2, paths, slopes, 2)

    part1 = bfs(start, end, nodesP1)
    part2 = bfs(start, end, nodesP2)

    if verbose:
        print(f"\nPart 1:\nLongest Path: {part1}\n\nPart 2:\nLongest Path: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
