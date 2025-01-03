import re


def part1(data):
    """ 2022 Day 5 Part 1

    >>> part1(['    [D]    ', '[N] [C]    ', '[Z] [M] [P]', ' 1   2   3 ', '', 'move 1 from 2 to 1', 'move 3 from 1 to 3', 'move 2 from 2 to 1', 'move 1 from 1 to 2'])
    'CMZ'
    """

    crates = []
    
    for n, line in enumerate(data):
        if len(line) == 0:
            ix = n + 1
            break

        for ix in range(1, len(line), 4):
            if line[ix] != ' ':
                while ix // 4 >= len(crates):
                    crates.append([])

                crates[ix // 4].append(line[ix])

    for i in range(len(crates)):
        crates[i].pop()
        crates[i].reverse()
    
    for line in data[ix:]:
        qty, start, dest = [int(x) for x in re.findall("\d+", line)]

        while qty != 0:
            qty -= 1
            crates[dest - 1].append(crates[start - 1].pop())

    return ''.join([crate[-1] for crate in crates])


def part2(data):
    """ 2022 Day 5 Part 2

    >>> part2(['    [D]    ', '[N] [C]    ', '[Z] [M] [P]', ' 1   2   3 ', '', 'move 1 from 2 to 1', 'move 3 from 1 to 3', 'move 2 from 2 to 1', 'move 1 from 1 to 2'])
    'MCD'
    """

    crates = []
    
    for n, line in enumerate(data):
        if len(line) == 0:
            ix = n + 1
            break

        for ix in range(1, len(line), 4):
            if line[ix] != ' ':
                while ix // 4 >= len(crates):
                    crates.append([])

                crates[ix // 4].append(line[ix])

    for i in range(len(crates)):
        crates[i].pop()
        crates[i].reverse()
    
    for line in data[ix:]:
        qty, start, dest = [int(x) for x in re.findall("\d+", line)]
        crates[dest - 1] += crates[start - 1][-qty:]
        crates[start - 1] = crates[start - 1][:-qty]

    return ''.join([crate[-1] for crate in crates])


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
        print(f"\nPart 1:\nCrates on top: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nCrates on top: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)