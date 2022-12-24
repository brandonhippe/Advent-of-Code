from time import perf_counter
from collections import defaultdict


DIR_MAP = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}


def moveBlizzards(blizzards, walls):
    newBlizzards = defaultdict(list)
    for b in blizzards.keys():
        for d in blizzards[b]:
            newB = tuple(p + o for p, o in zip(b, d))

            if newB in walls:
                newB = b
                while newB not in walls:
                    newB = tuple(p - o for p, o in zip(newB, d))

                newB = tuple(p + o for p, o in zip(newB, d))

            newBlizzards[newB].append(d)

    return newBlizzards


def bfs(start, end, blizzards, walls):
    states = {start}

    steps = 0
    while True:
        blizzards = moveBlizzards(blizzards, walls)
        newStates = set()
        for pos in states:
            if pos == end:
                return steps, blizzards

            for offset in [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]:
                newPos = tuple(p + o for p, o in zip(pos, offset))

                if newPos not in walls and newPos not in blizzards:
                    newStates.add(newPos)

        states = newStates
        steps += 1


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    blizzards = defaultdict(list)
    walls = set()
    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if l in DIR_MAP:
                blizzards[(x, y)].append(DIR_MAP[l])
            elif l == '#':
                walls.add((x, y))

    start = (lines[0].index('.'), 0)
    end = (lines[-1].index('.'), len(lines) - 1)

    walls.add((start[0], start[1] - 1))
    walls.add((end[0], end[1] + 1))

    part1, blizzards = bfs(start, end, blizzards, walls)

    r1, blizzards = bfs(end, start, blizzards, walls)
    r2, blizzards = bfs(start, end, blizzards, walls)
    part2 = part1 + r1 + 1 + r2 + 1

    if verbose:
        print(f"\nPart 1:\n{part1}\n\nPart 2:\n{part2}")

    
if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")