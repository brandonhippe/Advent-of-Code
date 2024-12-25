def part1(data, rows = 40):
    """ 2016 Day 18 Part 1

    >>> part1(['.^^.^.^^^^'], 10)
    38
    """

    first = '.' + data[0] + '.'

    safe = len([t for t in first if t == '.']) - 2
    pRow = first

    for _ in range(1, rows):
        rowText = ''
        for i in range(1, len(first) - 1):
            if pRow[i-1:i+2] in TILE_RULES:
                rowText += '^'
            else:
                rowText += '.'
                safe += 1

        pRow = '.' + rowText + '.'

    return safe


def part2(data):
    """ 2016 Day 18 Part 2
    """

    first = '.' + data[0] + '.'

    safe = len([t for t in first if t == '.']) - 2
    pRow = first

    for _ in range(1, 400000):
        rowText = ''
        for i in range(1, len(first) - 1):
            if pRow[i-1:i+2] in TILE_RULES:
                rowText += '^'
            else:
                rowText += '.'
                safe += 1

        pRow = '.' + rowText + '.'

    return safe


TILE_RULES = {'^^.', '.^^', '^..', '..^'}


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
        print(f"\nPart 1:\n{p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\n{p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)