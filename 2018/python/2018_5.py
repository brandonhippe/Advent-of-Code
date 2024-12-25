import re


def part1(data):
    """ 2018 Day 5 Part 1

    >>> part1(['dabAcCaCBAcCcaDA'])
    10
    """

    return len(reducePolymer(data[0]))


def part2(data):
    """ 2018 Day 5 Part 2

    >>> part2(['dabAcCaCBAcCcaDA'])
    4
    """

    word = reducePolymer(data[0])

    shortest = len(word)
    for c in range(ord('a'), ord('z') + 1):
        pattern = f"({chr(c)}|{chr(c).upper()})"
        tempPolymer = re.sub(pattern, '', word)
        length = len(reducePolymer(tempPolymer))
        if length < shortest:
            shortest = length

    return shortest


def reducePolymer(polymer):
    pattern = []
    for c in range(ord('a'), ord('z') + 1):
        pattern.append(chr(c) + chr(c).upper())
        pattern.append(chr(c).upper() + chr(c))

    pattern = f"({'|'.join(pattern)})"
    
    pPolymer = ''
    while pPolymer != polymer:
        pPolymer = polymer[:]

        polymer = re.sub(pattern, '', polymer)

    return polymer


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
        print(f"\nPart 1:\nLength of reduced polymer: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nLength of shortest reduced polyemer: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)