from functools import cache


def part1(data):
    """ 2017 Day 19 Part 1

    >>> part1(['     |          ', '     |  +--+    ', '     A  |  C    ', ' F---|----E|--+ ', '     |  |  |  D ', '     +B-+  +--+ '])
    'ABCDEF'
    """

    for y, line in enumerate(data):
        for x, l in enumerate(line):
            if y == 0 and l != ' ':
                start = (x, y)

    return pathFollow(start, tuple(data))[0]


def part2(data):
    """ 2017 Day 19 Part 2

    >>> part2(['     |          ', '     |  +--+    ', '     A  |  C    ', ' F---|----E|--+ ', '     |  |  |  D ', '     +B-+  +--+ '])
    38
    """

    for y, line in enumerate(data):
        for x, l in enumerate(line):
            if y == 0 and l != ' ':
                start = (x, y)

    return pathFollow(start, tuple(data))[1]


@cache
def pathFollow(start, lines):
    string = ''
    openList = [start]
    dir = (0, 1)
    steps = 0

    while len(openList) != 0:
        pos = openList.pop(0)
        if min(pos) < 0 or pos[0] >= len(lines[0]) or pos[1] >= len(lines):
            continue

        if lines[pos[1]][pos[0]] in '-|':
            openList.append(tuple([p + o for p, o in zip(pos, dir)]))
        elif lines[pos[1]][pos[0]] == '+':
            for pDir in [(dir[1], dir[0]), (dir[1], -dir[0]), (-dir[1], dir[0]), (-dir[1], -dir[0])]:
                newPos = tuple([p + o for p, o in zip(pos, pDir)])
                try:
                    if lines[newPos[1]][newPos[0]] != ' ':
                        dir = pDir
                        openList.append(newPos)
                        break
                except:
                    pass
        elif lines[pos[1]][pos[0]] != ' ':
            string += lines[pos[1]][pos[0]]
            openList.append(tuple([p + o for p, o in zip(pos, dir)]))

        steps += 1

    return (string, steps - 1)


def main(verbose = False):
    from pathlib import Path
    import sys, re
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from Modules.timer import Timer
    year, day = re.findall('\d+', str(__file__))[-2:]
    
    with open(Path(__file__).parent.parent.parent / f"Inputs/{year}_{day}.txt", encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    with Timer() as p1_time:
        p1 = part1(data)

    if verbose:
        print(f"\nPart 1:\nLetters collected: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nSteps: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)