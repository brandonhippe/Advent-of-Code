import time
import copy
import heapq

def manhatDist(p1, p2):
    return sum(abs(c1 - c2) for c1, c2 in zip(p1, p2))

def aStar(start, end, positions, numPos):
    openList = [[manhatDist(start, end), 0, start]]
    visited = {}

    while len(openList) != 0:
        currF, currG, pos = heapq.heappop(openList)
        
        if pos == end:
            return currG

        for n in [tuple(p + o for p, o in zip(pos, offset)) for offset in [[1, 0], [-1, 0], [0, 1], [0, -1]]]:
            if n not in positions or (n != end and n in numPos):
                continue

            nH, nG = manhatDist(n, end), currG + 1
            nF = nH + nG

            if n in visited and visited[n] <= nF:
                continue

            continuing = False
            for o in openList:
                if o[-1] == n and o[0] <= nF:
                    continuing = True
                    break

            if continuing:
                continue

            heapq.heappush(openList, [nF, nG, n])

        visited[pos] = currF

    return -1

def shortestPathP1(adjList, start, visited):
    visited[start] = True
    if False not in visited:
        visited[start] = False
        return 0

    shortest = float('inf')
    for n, l in enumerate(adjList[start]):
        if n == start or visited[n]:
            continue

        pathLen = shortestPathP1(adjList, n, visited) + l
        if pathLen < shortest:
            shortest = pathLen

    visited[start] = False

    return shortest

def shortestPathP2(adjList, start, visited):
    visited[start] = True
    if False not in visited:
        visited[start] = False
        return adjList[start][0]

    shortest = float('inf')
    for n, l in enumerate(adjList[start]):
        if n == start or visited[n]:
            continue

        pathLen = shortestPathP2(adjList, n, visited) + l
        if pathLen < shortest:
            shortest = pathLen

    visited[start] = False

    return shortest

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    numPos = {}
    positions = set()
    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if l != '#':
                positions.add((x, y))
            
            if l in '0123456789':
                numPos[(x, y)] = int(l)

    adjList = [[None] * len(numPos) for _ in range(len(numPos))]
    for k1, v1 in zip(numPos.keys(), numPos.values()):
        for k2, v2 in zip(numPos.keys(), numPos.values()):
            if adjList[v1][v2] is None:
                d = aStar(k1, k2, positions, numPos)
                adjList[v1][v2] = d
                adjList[v2][v2] = d

    print(f"\nPart 1:\nFewest steps to reach all numbers: {shortestPathP1(adjList, 0, [False] * len(adjList))}")
    print(f"\nPart 2:\nPossilbe fewest steps to reach all numbers and return to 0: {shortestPathP2(adjList, 0, [False] * len(adjList))}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} second.")
