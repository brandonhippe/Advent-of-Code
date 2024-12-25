def part1(data):
    """ 2022 Day 25 Part 1

    >>> part1(['1=-0-2', '12111', '2=0=', '21', '2=01', '111', '20012', '112', '1=-1=', '1-12', '12', '1=', '122'])
    '2=-1=0'
    """

    num = 0
    for line in data:
        mult = 1
        for c in line[::-1]:
            num += NUM[c] * mult
            mult *= 5

    p1 = []
    while num != 0:
        p1.append(num % 5)
        num //= 5

    for i, c in enumerate(p1):
        if c not in STRING:
            if i == len(p1) - 1:
                p1.append(0)

            p1[i + 1] += 1
            c -= 5

        p1[i] = STRING[c]

    return ''.join(reversed(p1))


def part2(data):
    """ 2022 Day 25 Part 2
    """

    return 1


NUM = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
STRING = {-2: '=', -1: '-', 0: '0', 1: '1', 2: '2'}


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
        print(f"\nPart 1:\nSNAFU Number: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nChristmas has been saved!\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)