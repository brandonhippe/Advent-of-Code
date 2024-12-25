def part1(data):
    """ 2022 Day 4 Part 1

    >>> part1(['2-4,6-8', '2-3,4-5', '5-7,7-9', '2-8,3-7', '6-6,4-6', '2-6,4-8'])
    2
    """

    pairs = [[[int(x) for x in pairs.split('-')] for pairs in line.split(',')] for line in data]

    overlaps = 0
    for a1, a2 in pairs:
        if (min(a1) <= min(a2) and max(a1) >= max(a2)) or (min(a2) <= min(a1) and max(a2) >= max(a1)):
            overlaps += 1
                
    return overlaps


def part2(data):
    """ 2022 Day 4 Part 2

    >>> part2(['2-4,6-8', '2-3,4-5', '5-7,7-9', '2-8,3-7', '6-6,4-6', '2-6,4-8'])
    4
    """

    pairs = [[[int(x) for x in pairs.split('-')] for pairs in line.split(',')] for line in data]

    overlaps = 0
    for a1, a2 in pairs:
        if min(a1) <= min(a2) <= max(a1) or min(a1) <= max(a2) <= max(a1) or min(a2) <= min(a1) <= max(a2) or min(a2) <= max(a1) <= max(a2):
            overlaps += 1

    return overlaps


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
        print(f"\nPart 1:\nOverlaping section assignments: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nOverlaping section assignments: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)