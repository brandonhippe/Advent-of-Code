from time import perf_counter
import heapq
from math import ceil, floor


def floodFill(pipes, startPos):
    openHeap = []
    openList = {}
    closedList = {}

    openHeap.append([0, startPos])
    openList[startPos] = 0

    while len(openList) != 0:
        q, pos = heapq.heappop(openHeap)
        del(openList[pos])

        for n in pipes[pos]:
            nF = q + 1

            if n in openList and openList[n] <= nF:
                continue

            if n in closedList and closedList[n] <= nF:
                continue

            heapq.heappush(openHeap, [nF, n])
            openList[n] = nF

        closedList[pos] = q

    return closedList


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    pipes = {}
    tiles = set()
    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if l == '|':
                pipes[(x, y)] = [(x, y - 1), (x, y + 1)]
            elif l == '-':
                pipes[(x, y)] = [(x - 1, y), (x + 1, y)]
            elif l == 'L':
                pipes[(x, y)] = [(x, y - 1), (x + 1, y)]
            elif l == 'J':
                pipes[(x, y)] = [(x, y - 1), (x - 1, y)]
            elif l == '7':
                pipes[(x, y)] = [(x, y + 1), (x - 1, y)]
            elif l == 'F':
                pipes[(x, y)] = [(x, y + 1), (x + 1, y)]
            elif l == 'S':
                animal = (x, y)
            else:
                tiles.add((x, y))

    pipes[animal] = []
    for pos, connects in pipes.items():
        if animal in connects and pos not in pipes[animal]:
            pipes[animal].append(pos)

    loop = floodFill(pipes, animal)
    part1 = max(loop.values())

    loop = set(loop.keys())
    
    for t in list(pipes.keys()):
        if t not in loop:
            tiles.add(t)
            del(pipes[t])

    part2 = 0

    for t in tiles:
        for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            pos = tuple(p + 0.5 * abs(o) for p, o in zip(t, offset[::-1]))
            count = 0
            while 0 <= pos[0] < len(lines[0]) and 0 <= pos[1] < len(lines):
                s1 = tuple(floor(c) for c in pos)
                s2 = tuple(ceil(c) for c in pos)

                if s1 in pipes and s2 in pipes and s2 in pipes[s1] and s1 in pipes[s2]:
                    count += 1

                pos = tuple(p + o for p, o in zip(pos, offset))

            if count % 2 == 1:
                part2 += 1
                break

    if verbose:
        print(f"\nPart 1:\nDistance to furthest point on loop: {part1}\n\nPart 2:\nTiles enclosed by loop: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
