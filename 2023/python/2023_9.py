import re


def part1(data):
    """ 2023 Day 9 Part 1

    >>> part1(['0 3 6 9 12 15', '1 3 6 10 15 21', '10 13 16 21 30 45'])
    114
    """

    return sum(extrapolate(seq) for seq in [[int(n) for n in re.findall('-?\d+', line)] for line in data])


def part2(data):
    """ 2023 Day 9 Part 2

    >>> part2(['0 3 6 9 12 15', '1 3 6 10 15 21', '10 13 16 21 30 45'])
    2
    """

    return sum(extrapolate(seq[::-1]) for seq in [[int(n) for n in re.findall('-?\d+', line)] for line in data])


def extrapolate(seq):
    if len(set(seq)) == 1:
        return seq[-1]
    
    diffs = [seq[i] - seq[i - 1] for i in range(1, len(seq))]
    return seq[-1] + extrapolate(diffs)


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
        print(f"\nPart 1:\nExtrapolated Value: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nReverse Extrapolated Value: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)