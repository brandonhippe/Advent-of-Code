def part1(data):
    """ 2022 Day 1 Part 1

    >>> part1(['1000', '2000', '3000', '', '4000', '', '5000', '6000', '', '7000', '8000', '9000', '', '10000'])
    24000
    """

    elves = [0]

    for line in data:
        if len(line) == 0:
            elves.append(0)
        else:
            elves[-1] += int(line)

    return max(elves)


def part2(data):
    """ 2022 Day 1 Part 2

    >>> part2(['1000', '2000', '3000', '', '4000', '', '5000', '6000', '', '7000', '8000', '9000', '', '10000'])
    45000
    """

    elves = [0]

    for line in data:
        if len(line) == 0:
            elves.append(0)
        else:
            elves[-1] += int(line)

    elves = sorted(elves, reverse=True)

    return sum(elves[:3])


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
        print(f"\nPart 1:\nMost calories carried: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nSum of calories carried by 3 highest: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)