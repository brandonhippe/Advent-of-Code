import time
import heapq

def manhatDist(p1, p2):
    return sum(abs(c1 - c2) for c1, c2 in zip(p1, p2))

def wall(pos, data):
    x, y = pos
    return len([c for c in bin(x*x + 3*x + 2*x*y + y + y*y + data)[2:] if c == '1']) % 2 == 1

def aStar(data, goal):
    openList = [[manhatDist((1, 1), goal), 0, (1, 1)]]
    visited = {}

    while len(openList) != 0:
        currF, currG, currPos = heapq.heappop(openList)

        if currPos == goal:
            return currG

        for n in [tuple(p + o for p, o in zip(currPos, offset)) for offset in [[0, 1], [0, -1], [1, 0], [-1, 0]]]:
            if min(n) < 0 or wall(n, data):
                continue

            nH, nG = manhatDist(n, goal), currG + 1
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

    return float('inf')

def main(data = 1362, goal = (31, 39)):
    print(f"\nPart 1:\nShortest path to {goal}: {aStar(data, goal)}")

    reachable = 0
    for rad in range(52):
        for c in range(rad + 1):
            reachable += 1 if not wall((rad, c), data) and aStar(data, (rad, c)) <= 50 else 0
            reachable += 1 if c != rad and not wall((rad, c), data) and aStar(data, (c, rad)) <= 50 else 0

    print(f"\nPart 2:\nPositions reached in at most 50 steps: {reachable}")
            

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
