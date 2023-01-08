from time import perf_counter
import sys
sys.path.insert(0,"C:/Users/Brandon Hippe/Documents/Coding Projects/Advent-of-Code/Modules")
from graphAlgorithms import bfs
        

def calcErosion(pos, erosionLevels, depth):
    if pos[0] == 0:
        return (pos[1] * 48271 + depth) % 20183

    if pos[1] == 0:
        return (pos[0] * 16807 + depth) % 20183

    p1 = (pos[0] - 1, pos[1])
    p2 = (pos[0], pos[1] - 1)

    if p1 not in erosionLevels:
        erosionLevels[p1] = calcErosion(p1, erosionLevels, depth)

    if p2 not in erosionLevels:
        erosionLevels[p2] = calcErosion(p2, erosionLevels, depth)

    return (erosionLevels[p1] * erosionLevels[p2] + depth) % 20183


def nextState(state, area, d, t, **kwargs):
    *pos, tool = state
    pos = tuple(pos)

    newStates = []

    for offset in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        nPos = tuple(p + o for p, o in zip(pos, offset))
        if min(nPos) < 0:
            continue

        if nPos not in area:
            area[nPos] = calcErosion(nPos, area, d)

        if tool == area[nPos] % 3:
            newTool = [t for t in range(3) if t != tool and t != area[pos] % 3]
            newState = tuple(list(pos) + newTool)
            newStates.append([newState, t + 7])
        else:
            newState = tuple(list(nPos) + [tool])
            newStates.append([newState, t + 1])

    return newStates


def abort(state, end, **kwargs):
    return state == end


def track(**kwargs):
    return None


def main(verbose):
    depth = 5913
    target = (8, 701)

    erosionLevels = {(0, 0): depth}

    erosionLevels[target] = calcErosion(target, erosionLevels, depth)
    erosionLevels[target] = depth

    part1 = sum(e % 3 for e in erosionLevels.values())
    part2 = bfs(startState = (0, 0, 1), end = tuple(list(target) + [1]), area = erosionLevels, d = depth, nextStateFunc = nextState, abortFunc = abort, trackFunc = track)

    if verbose:
        print(f"\nPart 1:\nRisk Level: {part1}\n\nPart 2:\nShortest time to reach target: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")