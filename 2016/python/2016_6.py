from collections import defaultdict


def part1(data):
    """ 2016 Day 6 Part 1

    >>> part1(['eedadn', 'drvtee', 'eandsr', 'raavrd', 'atevrs', 'tsrnev', 'sdttsa', 'rasrtv', 'nssdts', 'ntnada', 'svetve', 'tesnvt', 'vntsnd', 'vrdear', 'dvrsen', 'enarar'])
    'easter'
    """

    common = ''
    for i in range(len(data[0])):
        occurs = defaultdict(lambda: 0)
        for line in data:
            occurs[line[i]] += 1

        common += list(occurs.keys())[list(occurs.values()).index(max(occurs.values()))]

    return common


def part2(data):
    """ 2016 Day 6 Part 2

    >>> part2(['eedadn', 'drvtee', 'eandsr', 'raavrd', 'atevrs', 'tsrnev', 'sdttsa', 'rasrtv', 'nssdts', 'ntnada', 'svetve', 'tesnvt', 'vntsnd', 'vrdear', 'dvrsen', 'enarar'])
    'advent'
    """

    common = ''
    for i in range(len(data[0])):
        occurs = defaultdict(lambda: 0)
        for line in data:
            occurs[line[i]] += 1

        common += list(occurs.keys())[list(occurs.values()).index(min(occurs.values()))]

    return common


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
        print(f"\nPart 1:\nString composed of most common positional characters: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nString composed of least common positional characters: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)