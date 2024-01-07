import re


def part1(data):
    """ 2017 Day 6 Part 1

    >>> part1(['0, 2, 7, and 0'])
    5
    """

    banks = [int(x) for x in re.findall('\d+', data[0])]

    observed = set()
    steps = 0
    while tuple(banks) not in observed:
        observed.add(tuple(banks))

        moving = max(banks)
        ix = banks.index(moving)
        banks[ix] = 0

        while moving > 0:
            ix += 1
            ix %= len(banks)
            banks[ix] += 1
            moving -= 1

        steps += 1

    return steps


def part2(data):
    """ 2017 Day 6 Part 2

    >>> part2(['0, 2, 7, and 0'])
    4
    """

    banks = [int(x) for x in re.findall('\d+', data[0])]

    observed = set()
    steps = 0
    while tuple(banks) not in observed:
        observed.add(tuple(banks))

        moving = max(banks)
        ix = banks.index(moving)
        banks[ix] = 0

        while moving > 0:
            ix += 1
            ix %= len(banks)
            banks[ix] += 1
            moving -= 1

        steps += 1

    steps = 0
    observedRepeat = banks[:]
    while steps == 0 or observedRepeat != banks:
        moving = max(banks)
        ix = banks.index(moving)
        banks[ix] = 0

        while moving > 0:
            ix += 1
            ix %= len(banks)
            banks[ix] += 1
            moving -= 1

        steps += 1

    return steps


def main(verbose = False):
    from pathlib import Path
    import sys, re
    sys.path.append(str(Path(__file__).parent.parent))
    from Modules.timer import Timer
    year, day = re.findall('\d+', str(__file__))[-2:]
    
    with open(Path(__file__).parent.parent / f"Inputs/{year}_{day}.txt", encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    with Timer() as p1_time:
        p1 = part1(data)

    if verbose:
        print(f"\nPart 1:\nRedistribution cycles before repeat: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nLength of loop: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)