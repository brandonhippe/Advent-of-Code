import re


def part1(data):
    """ 2016 Day 1 Part 1

    R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks away.
    R2, R2, R2 leaves you 2 blocks due South of your starting position, which is 2 blocks away.
    R5, L5, R5, R3 leaves you 12 blocks away.

    >>> part1(['R2, L3'])
    5
    >>> part1(['R2, R2, R2'])
    2
    >>> part1(['R5, L5, R5, R3'])
    12
    """

    instructions = data[0].split(',')

    pos = (0, 0)
    facing = (0, -1)
    visited = {pos}

    for d in instructions:
        if 'L' in d:
            facing = (facing[1], -facing[0])
        else:
            facing = (-facing[1], facing[0])

        for _ in range(int(re.findall('\d+', d)[0])):
            pos = tuple(p + o for p, o in zip(pos, facing))

            visited.add(pos)

    return manhatDist(pos, [0] * len(pos))


def part2(data):
    """ 2016 Day 1 Part 2

    >>> part2(['R8, R4, R4, R8'])
    4
    """

    instructions = data[0].split(',')

    pos = (0, 0)
    facing = (0, -1)
    visited = {pos}
    firstRepeat = None

    for d in instructions:
        if 'L' in d:
            facing = (facing[1], -facing[0])
        else:
            facing = (-facing[1], facing[0])

        for _ in range(int(re.findall('\d+', d)[0])):
            pos = tuple(p + o for p, o in zip(pos, facing))

            if pos in visited and firstRepeat is None:
                firstRepeat = pos
                break

            visited.add(pos)

        if firstRepeat:
            break

    return manhatDist(firstRepeat, [0] * len(firstRepeat))


def manhatDist(p1, p2):
    return sum([abs(c1 - c2) for c1, c2 in zip(p1, p2)])


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
        print(f"\nPart 1:\nDistance to Easter Bunny HQ: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nDistance to first repeated position: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)