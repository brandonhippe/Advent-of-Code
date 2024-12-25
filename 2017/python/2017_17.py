from collections import deque


def part1(data):
    """ 2017 Day 17 Part 1

    >>> part1(['3'])
    638
    """

    num = int(data[0])
    buf = deque([])

    for i in range(2018):
        buf.rotate(-num)
        buf.append(i)

    return buf[0]


def part2(data):
    """ 2017 Day 17 Part 2
    """

    num = int(data[0])
    buf = deque([])

    for i in range(50_000_001):
        buf.rotate(-num)
        buf.append(i)

    return buf[(buf.index(0) + 1) % len(buf)]


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
        print(f"\nPart 1:\nNumber after 2017: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nNumber after 50,000,000: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)