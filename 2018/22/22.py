import time
import heapq

class searchNode:
    def __init__(self, pos, end, prev = None):
        self.pos = pos
        self.moves = [tuple([p + o for p, o in zip(self.pos, offset)] + [self.pos[-1]]) for offset in [[1, 0], [-1, 0], [0, 1], [0, -1]]]
        self.swaps = [tuple(list(pos[:-1]) + [l]) for l in range(3) if l != self.pos[-1]]
        self.h = self.heuristic(end)
        self.g = 0 if prev is None else (prev.g + (1 if self.pos[-1] == prev.pos[-1] else 7))
        self.f = self.g + self.h        

    def heuristic(self, target):
        layerOffset = 7 if self.pos[-1] != target[-1] else 0
        return sum([abs(p - t) for p, t in zip(self.pos[:-1], target[:-1])]) + layerOffset

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
        return (self.f < other.f) or (self.f == other.f and self.h < other.h)

def erosionLevel(pos, depth, target, calculated):
    if pos not in calculated:
        if pos == target:
            calculated[pos] = depth % 20183
        elif 0 in pos:
            calculated[pos] = (sum(p * m for p, m in zip(pos, (16807, 48271))) + depth) % 20183
        else:
            calculated[pos] = ((erosionLevel((pos[0] - 1, pos[1]), depth, target, calculated) * erosionLevel((pos[0], pos[1] - 1), depth, target, calculated)) + depth) % 20183

    return calculated[pos]

def shortestPath(start, end, erosionLevels, depth):
    # 0: Neither, 1: Torch, 2: Climbing gear
    visited = {}
    openList = [searchNode(start, end)]

    while len(openList) != 0:
        currPos = heapq.heappop(openList)

        if currPos.pos == end:
            return currPos.g

        visited[currPos] = currPos.f

        for n in currPos.moves + currPos.swaps:
            newPos = searchNode(n, end, currPos)
            if (newPos in visited and visited[newPos] <= newPos.f) or (newPos in openList and openList[openList.index(newPos)].f <= newPos.f) or (min(newPos.pos) < 0) or (erosionLevel(newPos.pos[:-1], depth, end[:-1], erosionLevels) % 3 == newPos.pos[-1]):
                continue

            heapq.heappush(openList, newPos)

    return -1

def main(depth = 5913, target = (8, 701)):
    print(f"{depth = }, {target = }")

    erosionLevels = {}
    regions = {(x, y): erosionLevel((x, y), depth, target, erosionLevels) % 3 for x in range(target[0] + 1) for y in range(target[1] + 1)}

    print(f"\nPart 1:\nTotal risk level: {sum(regions.values())}")
    print(f"\nPart 2:\nTime for shortest path to target: {shortestPath((0, 0, 1), tuple(list(target) + [1]), erosionLevels, depth)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
