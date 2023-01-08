from time import perf_counter
from collections import defaultdict


def main(verbose):
    with open("input.txt", encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    walls = set()
    area = set()
    start = None
    for y, line in enumerate(lines):
        if len(line) == 0:
            break

        for x, l in enumerate(line):
            if l == '.':
                if y == 0 and start is None:
                    start = (x, y)

                area.add((x, y))
            elif l == '#':
                walls.add((x, y))

    wrapAround = defaultdict(dict)
    for pos in area:
        for offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nPos = tuple(p + o for p, o in zip(pos, offset))

            if nPos in area or nPos in walls:
                continue

            nPos = tuple(p - o for p, o in zip(pos, offset))
            while nPos in area or nPos in walls:
                nPos = tuple(p - o for p, o in zip(nPos, offset))

            wrapAround[pos][offset] = tuple(p + o for p, o in zip(nPos, offset))

    pos = start[:]
    facing = (1, 0)
    inProgress = ''
    for c in lines[-1] + 'R':
        if c in 'LR':
            amt = int(inProgress)
            inProgress = ''

            while amt != 0:
                if facing in wrapAround[pos]:
                    newPos = wrapAround[pos][facing]
                else:
                    newPos = tuple(p + o for p, o in zip(pos, facing))

                if newPos in walls:
                    break

                pos = newPos
                amt -= 1

            if c == 'L':
                facing = (facing[1], -facing[0])
            elif c == 'R':
                facing = (-facing[1], facing[0])
        else:
            inProgress += c
    
    facing = (facing[1], -facing[0])
    facingScore = {(1, 0): 0, (0, 1): 1, (-1, 0): 2, (0, -1): 3}

    part1 = (1000 * (pos[1] + 1)) + (4 * (pos[0] + 1)) + facingScore[facing]

    # RIGHT: (1, 0), LEFT: (-1, 0), UP: (0, -1), DOWN: (0, 1)
    wrapAround = defaultdict(dict)
    for i in range(0, 50):
        wrapAround[(i, 199)][(0, 1)] = [(i + 100, 0), (0, 1)]
        wrapAround[(149, i)][(1, 0)] = [(99, 149 - i), (-1, 0)]
        wrapAround[(i, 100)][(0, -1)] = [(50, i + 50), (1, 0)]
        wrapAround[(50, i)][(-1, 0)] = [(0, 149 - i), (1, 0)]

    for i in range(50, 100):
        wrapAround[(i, 0)][(0, -1)] = [(0, 100 + i), (1, 0)]
        wrapAround[(i, 149)][(0, 1)] = [(49, 100 + i), (-1, 0)]
        wrapAround[(99, i)][(1, 0)] = [(i + 50, 49), (0, -1)]
        wrapAround[(50, i)][(-1, 0)] = [(i - 50, 100), (0, 1)]

    for i in range(100, 150):
        wrapAround[(i, 0)][(0, -1)] = [(i - 100, 199), (0, -1)]
        wrapAround[(99, i)][(1, 0)] = [(149, 49 - (i - 100)), (-1, 0)]
        wrapAround[(i, 49)][(0, 1)] = [(99, i - 50), (-1, 0)]
        wrapAround[(0, i)][(-1, 0)] = [(50, 49 - (i - 100)), (1, 0)]

    for i in range(150, 200):
        wrapAround[(49, i)][(1, 0)] = [(i - 100, 149), (0, -1)]
        wrapAround[(0, i)][(-1, 0)] = [(i - 100, 0), (0, 1)]

    pos = start[:]
    facing = (1, 0)
    inProgress = ''
    for c in lines[-1] + 'R':
        if c in 'LR':
            amt = int(inProgress)
            inProgress = ''

            while amt != 0:
                if facing in wrapAround[pos]:
                    newPos, newFacing = wrapAround[pos][facing]
                else:
                    newPos = tuple(p + o for p, o in zip(pos, facing))
                    newFacing = facing

                if newPos in walls:
                    break

                pos = newPos
                facing = newFacing
                amt -= 1

            if c == 'L':
                facing = (facing[1], -facing[0])
            elif c == 'R':
                facing = (-facing[1], facing[0])
        else:
            inProgress += c
    
    facing = (facing[1], -facing[0])
    facingScore = {(1, 0): 0, (0, 1): 1, (-1, 0): 2, (0, -1): 3}

    part2 = (1000 * (pos[1] + 1)) + (4 * (pos[0] + 1)) + facingScore[facing]

    if verbose:
        print(f"\nPart 1:\n{part1}\n\nPart 2:\n{part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")