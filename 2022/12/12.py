from time import perf_counter
import heapq


def manhatDist(p1, p2):
    return sum([abs(c1 - c2) for c1, c2 in zip(p1, p2)])


def aStar(height, start, end):
    openList = [[manhatDist(start, end), 0, start]]
    openDict = {start: manhatDist(start, end)}
    closedDict = {}

    while len(openList) != 0:
        f, g, pos = heapq.heappop(openList)

        if pos in openDict:
            del(openDict[pos])
        else:
            continue

        if pos == end:
            return g

        for noff in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            nPos = tuple(p + n for p, n in zip(pos, noff))

            if nPos not in height or height[nPos] - height[pos] > 1:
                continue

            nG, nH = g + 1, manhatDist(nPos, end)
            nF = nG + nH

            if (nPos in openDict and openDict[nPos] <= nF) or (nPos in closedDict and closedDict[nPos] <= nF):
                continue

            heapq.heappush(openList, [nF, nG, nPos])
            openDict[nPos] = nF

        closedDict[pos] = f

    return float('inf')


def main(filename):
    with open(filename, encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    height = {}
    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if l == "S":
                height[(x, y)] = 0
                start = (x, y)
            elif l == "E":
                height[(x, y)] = 25
                end = (x, y)
            else:
                height[(x, y)] = ord(l) - ord('a')

    print(f"\nPart 1:\nFewest steps from start to summit: {aStar(height, start, end)}")

    minLen = float('inf')
    for pos, h in zip(height.keys(), height.values()):
        if h == 0:
            minLen = min(minLen, aStar(height, pos, end))

    print(f"\nPart 2:\nShortest scenic path: {minLen}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input.txt")
    print(f"\nRan in {perf_counter() - init_time} seconds.")