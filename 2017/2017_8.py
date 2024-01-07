from collections import defaultdict


def part1(data):
    """ 2017 Day 8 Part 1

    >>> part1(['b inc 5 if a > 1', 'a inc 1 if b < 5', 'c dec -10 if a >= 1', 'c inc -20 if c == 10'])
    1
    """

    registers = defaultdict(lambda: 0)
    for ins in data:
        ins = ins.replace('\n', '')
        ins += 'else 0\n'
        ins = ins.replace('inc', '+=')
        ins = ins.replace('dec', '-=')

        exec(ins, {}, registers)
        thisMax = max(registers.values())

    return max(registers.values())


def part2(data):
    """ 2017 Day 8 Part 2

    >>> part2(['b inc 5 if a > 1', 'a inc 1 if b < 5', 'c dec -10 if a >= 1', 'c inc -20 if c == 10'])
    10
    """

    registers = defaultdict(lambda: 0)
    maxVal = float('-inf')
    for ins in data:
        ins = ins.replace('\n', '')
        ins += 'else 0\n'
        ins = ins.replace('inc', '+=')
        ins = ins.replace('dec', '-=')

        exec(ins, {}, registers)
        thisMax = max(registers.values())
        if thisMax > maxVal:
            maxVal = thisMax

    return maxVal


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
        print(f"\nPart 1:\nMaximum value in any register: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nMaximum value in any register at any point: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)