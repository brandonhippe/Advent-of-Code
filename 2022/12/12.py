from time import perf_counter


def bfs(height, start, end):
    openList = [[start, 0]]
    openSet = {start}
    closedSet = set()

    while len(openList) != 0:
        pos, g = openList.pop(0)
        openSet.remove(pos)

        if (isinstance(end, int) and height[pos] == end) or (isinstance(end, tuple) and pos == end):
            return g

        for noff in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            nPos = tuple(p + n for p, n in zip(pos, noff))

            if nPos not in height or (isinstance(end, int) and height[pos] - height[nPos] > 1) or (isinstance(end, tuple) and height[nPos] - height[pos] > 1) or nPos in openSet or nPos in closedSet:
                continue

            openList.append([nPos, g + 1])
            openSet.add(nPos)

        closedSet.add(pos)


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

    print(f"\nPart 1:\nFewest steps from start to summit: {bfs(height, start, end)}")
    print(f"\nPart 2:\nShortest scenic path: {bfs(height, end, 0)}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input.txt")
    print(f"\nRan in {perf_counter() - init_time} seconds.")