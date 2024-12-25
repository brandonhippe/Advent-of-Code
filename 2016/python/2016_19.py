def part1(data):
    """ 2016 Day 19 Part 1

    >>> part1(['5'])
    3
    """

    return int(bin(int(data[0]))[3:] + bin(int(data[0]))[2:3], 2)


def part2(data):
    """ 2016 Day 19 Part 2

    >>> part2(['5'])
    2
    """

    num = int(data[0])
    x = 1
    while x * 3 < num:
        x *= 3

    return num - x if num <= 2 * x else x + 2 * (num - (2 * x))


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
        print(f"\nPart 1:\nElf that steals all gifts: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nElf that steals all gifts: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)