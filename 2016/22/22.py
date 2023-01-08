import time
import re
import heapq

class Node:
    def __init__(self, x, y, inpNums):
        self.startPos = (x, y)
        self.size, self.used, self.avail, self.percent = inpNums
        self.used = (self.used, self.startPos)

    def __lt__(self, other):
        return self.percent < other.percent

def manhatDist(p1, p2):
    return sum(abs(c1 - c2) for c1, c2 in zip(p1, p2))

def aStar(nodes, start, end, avgLen):
    openList = [[manhatDist(start, end), 0, start]]
    visited = {}

    while len(openList) != 0:
        currF, currG, currPos = heapq.heappop(openList)

        if currPos == end:
            return currG

        for n in [tuple(p + o for p, o in zip(currPos, offset)) for offset in [[0, 1], [0, -1], [1, 0], [-1, 0]]]:
            if n not in nodes or len(str(nodes[n].used[0])) > avgLen:
                continue

            nH, nG = manhatDist(n, end), currG + 1
            nF = nH + nG

            if n in visited and visited[n] <= nF:
                continue

            continuing = False
            for o in openList:
                if n == o[2] and nF >= o[0]:
                    continuing = True
                    break

            if continuing:
                continue

            heapq.heappush(openList, [nF, nG, n])

        visited[currPos] = currF

    return -1

def dataPath(nodes, goalNode):
    avgUsedLen = len(str(sum(n.used[0] for n in nodes.values()) // len(nodes)))
    minNode = list(nodes.keys())[[n.used[0] for n in nodes.values()].index(min(n.used[0] for n in nodes.values()))]

    steps = aStar(nodes, minNode, goalNode, avgUsedLen)
    while goalNode != (1, 0):
        steps += 5
        goalNode = (goalNode[0] - 1, 0)

    return steps

def main(verbose):
    goalNode = (-1, 0)
    with open("input.txt", encoding='UTF-8') as f:
        nodes = {}
        for line in f.readlines()[2:]:
            x, y, *otherNums = [int(n) for n in re.findall('\d+', line)]
            nodes[(x, y)] = Node(x, y, otherNums)
            if y == 0 and x > goalNode[0]:
                goalNode = (x, y)

    pairs = 0
    for n1 in nodes.values():
        for n2 in nodes.values():
            if n1 == n2:
                continue

            pairs += 1 if n1.used[0] > 0 and n2.avail >= n1.used[0] else 0

    part2 = dataPath(nodes, goalNode)

    if verbose:
        print(f"\nPart 1:\nNumber of viable pairs of nodes: {pairs}\n\nPart 2:\nFewest steps to access data: {part2}")

    return [pairs, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
