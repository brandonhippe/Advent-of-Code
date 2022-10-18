import time
import heapq
from collections import defaultdict


def manhatDist(p1, p2):
    return sum([abs(c1 - c2) for c1, c2 in zip(p1, p2)])


def aStar(start, end, area):
    openList = [[manhatDist(start, end), 0, start]]
    gScores = defaultdict(lambda: float('inf'))
    closedList = set()

    while len(openList) > 0:
        _, qG, qPos = heapq.heappop(openList)

        if qPos == end:
            return qG

        if qPos in closedList:
            continue

        for nOff in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            nPos = tuple(c1 + c2 for c1, c2 in zip(qPos, nOff))

            if nPos not in area or nPos in closedList:
                continue

            nG = qG + area[nPos]

            if nG < gScores[nPos]:
                heapq.heappush(openList, [nG + manhatDist(nPos, end), nG, nPos])
                gScores[nPos] = nG

        closedList.add(qPos)

    return -1


def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = [[int(x) for x in line.strip()] for line in f.readlines()]

    area = {}
    for y, line in enumerate(data):
        for x, l in enumerate(line):
            area[tuple([x, y])] = l

    print(f"\nPart 1:\nSafest path risk: {aStar((0, 0), (len(data) - 1, len(data) - 1), area)}")

    areaP2 = {}
    for y in range(len(data) * 5):
        for x in range(len(data) * 5):
            if tuple([x, y]) in area:
                areaP2[tuple([x, y])] = area[tuple([x, y])]
            else:
                increment = manhatDist([x, y], [x % len(data), y % len(data)]) // len(data)
                areaP2[tuple([x, y])] = ((area[tuple([x % len(data), y % len(data)])] - 1 + increment) % 9) + 1

    print(f"\nPart 2:\nSafest path risk: {aStar((0, 0), (len(data) * 5 - 1, len(data) * 5 - 1), areaP2)}")


if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
