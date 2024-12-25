import re


def part1(data):
    """ 2017 Day 15 Part 1

    >>> part1(['generator A uses 65', 'generator B uses 8921'])
    588
    """

    a, b = [[int(x) for x in re.findall('\d+', line)][0] for line in data]
    aMult, bMult = 16807, 48271
    
    count = 0
    for _ in range(40_000_000):
        a = (a * aMult) % 2147483647
        b = (b * bMult) % 2147483647

        count += a & (0xFFFF) == b & (0xFFFF)

    return count


def part2(data):
    """ 2017 Day 15 Part 2

    >>> part2(['generator A uses 65', 'generator B uses 8921'])
    309
    """

    a, b = [[int(x) for x in re.findall('\d+', line)][0] for line in data]
    aMult, bMult = 16807, 48271

    count = 0
    for _ in range(5_000_000):
        while True:
            a = (a * aMult) % 2147483647

            if not a & 3:
                break

        while True:
            b = (b * bMult) % 2147483647

            if not b & 7:
                break

        count += a & (0xFFFF) == b & (0xFFFF)

    return count


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
        print(f"\nPart 1:\nMatches for 40 million pairs: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nMatches for 5 million pairs: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)