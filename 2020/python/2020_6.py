from collections import defaultdict


def part1(data):
    """ 2020 Day 6 Part 1

    >>> part1(['abc', '', 'a', 'b', 'c', '', 'ab', 'ac', '', 'a', 'a', 'a', 'a', '', 'b', ''])
    11
    """

    count = 0
    group = defaultdict(lambda: 0)
    inGroup = 0
    for line in data:
        if len(line) == 0:
            count += len(group)

            group = defaultdict(lambda: 0)
            inGroup = 0
            continue
        
        inGroup += 1
        for c in line:
            group[c] += 1

    return count


def part2(data):
    """ 2020 Day 6 Part 2

    >>> part2(['abc', '', 'a', 'b', 'c', '', 'ab', 'ac', '', 'a', 'a', 'a', 'a', '', 'b', ''])
    6
    """

    count = 0
    group = defaultdict(lambda: 0)
    inGroup = 0
    for line in data:
        if len(line) == 0:
            count += len([g for g in list(group.keys()) if group[g] == inGroup])

            group = defaultdict(lambda: 0)
            inGroup = 0
            continue
        
        inGroup += 1
        for c in line:
            group[c] += 1

    return count


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
        print(f"\nPart 1:\nNumber of questions answered yes: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nNumber of questions answered yes by everyone in a group: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)