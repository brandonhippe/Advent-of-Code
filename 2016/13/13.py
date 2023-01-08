import time
import heapq

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

def main(verbose):
    data = 1362
    goal = (31, 39)

    part1 = aStar(data, goal)
    part2 = aStar(data)
    
    if verbose:
        print(f"\nPart 1:\nShortest path to {goal}: {part1}\n\nPart 2:\nPositions reached in at most 50 steps: {part2}")

    return [part1, part2]
            

if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
