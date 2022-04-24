import time
import heapq

def erosionLevel(pos, depth, target, calculated):
    if pos not in calculated:
        if pos == target:
            calculated[pos] = depth % 20183
        elif 0 in pos:
            calculated[pos] = (sum(p * m for p, m in zip(pos, (16807, 48271))) + depth) % 20183
        else:
            calculated[pos] = ((erosionLevel((pos[0] - 1, pos[1]), depth, target, calculated) * erosionLevel((pos[0], pos[1] - 1), depth, target, calculated)) + depth) % 20183

    return calculated[pos]

def heuristic(pos, target):
    layerOffset = 7 if pos[-1] != target[-1] else 0
    return sum([abs(p - t) for p, t in zip(pos[:-1], target[:-1])]) + layerOffset

def aStar(start, end, regions):
    # 0: Neither, 1: Torch, 2: Climbing gear
    visited = {tuple(list(pos) + [r]): float('-inf') for pos, r in zip(regions.keys(), regions.values())}
    openList = [[heuristic(start, end), 0, start]]

    while len(openList) != 0:
        currF, currG, currPos = heapq.heappop(openList)

        if currPos == end:
            return currG

        for n in [tuple([p + o for p, o in zip(currPos[:-1], offset)] + [currPos[-1]]) for offset in [[1, 0], [-1, 0], [0, 1], [0, -1]]] + [tuple(list(currPos[:-1]) + [(currPos[-1] + l) % 3]) for l in [-1, 1]]:
            nH = heuristic(n, end)
            if n[-1] == currPos[-1]:
                nG = currG + 1
            else:
                nG = currG + 7

            nF = nG + nH

            adding = True
            for o in openList:
                if o[2] == n and o[0] <= nF:
                    adding = False
                    break

            if not adding:
                continue

            if n in visited:
                foundF = visited[n]
                if foundF <= nF:
                    continue

            heapq.heappush(openList, [nF, nG, n])

        visited[currPos] = currF

    return -1

def main(depth = 5913, target = (8, 701)):
    print(f"{depth = }, {target = }")

    erosionLevels = {}
    regions = {(x, y): erosionLevel((x, y), depth, target, erosionLevels) % 3 for x in range(target[0] + 1) for y in range(target[1] + 1)}

    print(f"\nPart 1:\nTotal risk level: {sum(regions.values())}")
    print(f"\nPart 2:\nTime for shortest path to target: {aStar((0, 0, 1), tuple(list(target) + [1]), regions)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main(510, (10, 10))
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
