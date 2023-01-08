from time import perf_counter
import sys
sys.path.insert(0,"C:/Users/Brandon Hippe/Documents/Coding Projects/Advent-of-Code/Modules")
from graphAlgorithms import bfs


def nextState(state, height, t, **kwargs):
    newStates = []

    for nOff in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        nPos = tuple(p + o for p, o in zip(state, nOff))

        if nPos in height and height[state] - height[nPos] <= 1:
            newStates.append([nPos, t + 1])

    return newStates


def main(verbose):
    with open("input.txt", encoding="UTF-8") as f:
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

    part1, part2 = bfs(startState = end, end = start, height = height, nextStateFunc = nextState, abortFunc = lambda state, end, **kwargs: state == end, trackFunc = lambda state, t, tracked, height, **kwargs: t if tracked is None and height[state] == 0 else tracked)

    if verbose:
        print(f"\nPart 1:\nFewest steps from start to summit: {part1}\n\nPart 2:\nShortest scenic path: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")