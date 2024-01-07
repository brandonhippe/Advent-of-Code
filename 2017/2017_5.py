def part1(data):
    """ 2017 Day 5 Part 1

    >>> part1(['0', '3', '0', '1', '-3'])
    5
    """

    lines = [int(line) for line in data]

    ix = 0
    steps = 0
    while 0 <= ix < len(lines):
        jmp = lines[ix]
        lines[ix] += 1
        ix += jmp
        steps += 1

    return steps


def part2(data):
    """ 2017 Day 5 Part 2

    >>> part2(['0', '3', '0', '1', '-3'])
    10
    """

    lines = [int(line) for line in data]

    ix = 0
    steps = 0
    while 0 <= ix < len(lines):
        jmp = lines[ix]
        lines[ix] += 1 if lines[ix] < 3 else -1
        ix += jmp
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
        print(f"\nPart 1:\nSteps before jumping outside list: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nSteps before jumping outside list: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)