import numpy as np


def part1(data):
    """ 2018 Day 11 Part 1

    >>> part1(['42'])
    '21,61'
    """

    serialNo = int(data[0])
    grid = np.fromfunction(lambda x, y: ((((((y + 1) * ((x + 1) + 10)) + serialNo) * ((x + 1) + 10)) // 100) % 10) - 5, (300, 300), dtype=int)

    
    sz = 3
    squares = sum([grid[x:x - sz + 1 or None, y:y - sz + 1 or None] for x in range(sz) for y in range(sz)])
    maxPower = squares.max()
    location = np.concatenate(np.where(squares == maxPower))
    
    return printLoc(location)


def part2(data):
    """ 2018 Day 11 Part 2

    >>> part2(['18'])
    '90,269,16'
    >>> part2(['42'])
    '232,251,12'
    """

    serialNo = int(data[0])
    grid = np.fromfunction(lambda x, y: ((((((y + 1) * ((x + 1) + 10)) + serialNo) * ((x + 1) + 10)) // 100) % 10) - 5, (300, 300), dtype=int)

    overallMax = float('-inf')
    increased = []
    for sz in range(3, 301):
        increased.append(False)
        squares = sum([grid[x:x - sz + 1 or None, y:y - sz + 1 or None] for x in range(sz) for y in range(sz)])
        maxPower = squares.max()
        location = np.concatenate(np.where(squares == maxPower))
            
        if maxPower > overallMax:
            overallMax = maxPower
            loc = np.concatenate((location, np.full(1, sz - 1)))
            increased[-1] = True

        if True not in increased[-3:]:
            break
    
    return printLoc(loc)


def printLoc(loc):
    return ",".join(str(c + 1) for c in loc)


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
        print(f"\nPart 1:\nLocation of maximum power: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nLocation of maximum power: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)