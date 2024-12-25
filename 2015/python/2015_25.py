import re


def part1(data):
    """ 2015 Day 25 Part 1
    """

    pos = [int(x) for x in re.findall('\d+', data[0])]
    diagIndex = triangle(sum(pos) - 1) - (sum(pos) - 1 - pos[1])
    return (20151125 * pow(252533, diagIndex - 1, 33554393)) % 33554393


def part2(data):
    """ 2015 Day 25 Part 2
    """

    return 1


def triangle(n):
    return n * (n + 1) // 2


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
        print(f"\nPart 1:\nCode to give the machine: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nChristmas has been saved!\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)