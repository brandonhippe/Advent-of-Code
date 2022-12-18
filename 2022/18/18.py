from time import perf_counter
import re
from collections import deque


def bfs(start, mins, maxs, cubes):
    openList = deque([start])
    openSet = {start}
    visited = set()

    while len(openList) != 0:
        pos = openList.pop()

        if pos in openSet:
            openSet.remove(pos)
        else:
            continue

        for offset in [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]:
            oCube = tuple(p + o for p, o in zip(pos, offset))
            if oCube not in cubes and oCube not in openSet and oCube not in visited and all(oCube[i] >= mins[i] and oCube[i] <= maxs[i] for i in range(3)):
                openList.appendleft(oCube)
                openSet.add(oCube)

        visited.add(pos)

    return visited


def main(filename):
    with open(filename, encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    cubes = set(tuple(int(x) for x in re.findall('-?\d+', line)) for line in lines)

    cubeFaces = {c: [True] * 6 for c in cubes}
    for c in cubes:
        for i, offset in enumerate([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]):
            if tuple(p + o for p, o in zip(c, offset)) in cubeFaces:
                cubeFaces[tuple(p + o for p, o in zip(c, offset))][i] = False
 
    print(f"\nPart 1:\nTotal surface area: {sum(sum(cF) for cF in cubeFaces.values())}")

    possible = set()
    for c in cubes:
        for offset in [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]:
            oCube = tuple(p + o for p, o in zip(c, offset))
            if oCube not in cubes and oCube not in possible:
                possible.add(oCube)

    mins = tuple(min(c[i] for c in cubes) - 1 for i in range(3))
    maxs = tuple(max(c[i] for c in cubes) + 1 for i in range(3))

    outside = possible.intersection(bfs(mins, mins, maxs, cubes))
    possible = possible.difference(outside)

    for c in possible:
        for i, offset in enumerate([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]):
            if tuple(p + o for p, o in zip(c, offset)) in cubeFaces:
                cubeFaces[tuple(p + o for p, o in zip(c, offset))][i] = False

    print(f"\nPart 2:\nExterior surface area: {sum(sum(cF) for cF in cubeFaces.values())}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input.txt")
    print(f"\nRan in {perf_counter() - init_time} seconds.")