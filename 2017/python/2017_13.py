import re


def part1(data):
    """ 2017 Day 13 Part 1

    >>> part1(['0: 3', '1: 2', '4: 4', '6: 4'])
    24
    """

    scanners = {k: v for k, v in [[int(x) for x in re.findall('\d+', line)] for line in data]}
    return sum(scanner * depth if not scanner % (2 * (depth - 1)) else 0 for scanner, depth in scanners.items())


def part2(data):
    """ 2017 Day 13 Part 2

    >>> part2(['0: 3', '1: 2', '4: 4', '6: 4'])
    10
    """

    scanners = {k: v for k, v in [[int(x) for x in re.findall('\d+', line)] for line in data]}

    i = 0
    finished = False
    while not finished:
        finished = True
        for scanner, depth in scanners.items():
            if (i + scanner) % (2 * (depth - 1)) == 0:
                finished = False
                break

        i += 1

    return i - 1


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
        print(f"\nPart 1:\nTrip severity: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nDelay in picoseconds: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)