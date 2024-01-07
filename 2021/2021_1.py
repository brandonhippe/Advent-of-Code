def part1(data):
    """ 2021 Day 1 Part 1

    >>> part1(['199', '200', '208', '210', '200', '207', '240', '269', '260', '263'])
    7
    """

    return len([i for i in range(1, len(data)) if int(data[i]) > int(data[i - 1])])


def part2(data):
    """ 2021 Day 1 Part 2

    >>> part2(['199', '200', '208', '210', '200', '207', '240', '269', '260', '263'])
    5
    """

    lines = [int(n) for n in data]

    increased = 0
    for i in range(3, len(lines)):
        sums = [0] * 2
        frame1 = lines[i - 3:i]
        frame2 = lines[i - 2:i + 1]
        for j in range(3):
            sums[0] += frame1[j]
            sums[1] += frame2[j]

        if sums[1] > sums[0]:
            increased += 1

    return increased


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
        print(f"\nPart 1:\nNumber of increases: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nNumber of increases: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)