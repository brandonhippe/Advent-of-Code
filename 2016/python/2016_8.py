import numpy as np
import re


def part1(data, rows = 6, cols = 50):
    """ 2016 Day 8 Part 1

    >>> part1(['rect 3x2', 'rotate column x=1 by 1', 'rotate row y=0 by 4', 'rotate column x=1 by 1'], 3, 7)
    6
    """

    screen = np.zeros((rows, cols), dtype=int)
    
    for line in data:
        if line[1] == 'e':
            c, r = [int(x) for x in re.findall('\d+', line)]
            screen[0:r, 0:c] = 1
        elif 'x' in line:
            c, amt = [int(x) for x in re.findall('\d+', line)]
            screen = np.concatenate((screen[:, :c], np.transpose(np.atleast_2d(np.concatenate((screen[-amt:, c], screen[:-amt, c])))), screen[:, c+1:]), axis=1)
        elif 'y' in line:
            r, amt = [int(x) for x in re.findall('\d+', line)]
            screen = np.concatenate((screen[:r, :], np.atleast_2d(np.concatenate((screen[r, -amt:], screen[r, :-amt]))), screen[r+1:, :]), axis=0)

    return sum(screen.flat)


def part2(data, rows = 6, cols = 50):
    """ 2016 Day 8 Part 2
    """

    screen = np.zeros((rows, cols), dtype=int)
    
    for line in data:
        if line[1] == 'e':
            c, r = [int(x) for x in re.findall('\d+', line)]
            screen[0:r, 0:c] = 1
        elif 'x' in line:
            c, amt = [int(x) for x in re.findall('\d+', line)]
            screen = np.concatenate((screen[:, :c], np.transpose(np.atleast_2d(np.concatenate((screen[-amt:, c], screen[:-amt, c])))), screen[:, c+1:]), axis=1)
        elif 'y' in line:
            r, amt = [int(x) for x in re.findall('\d+', line)]
            screen = np.concatenate((screen[:r, :], np.atleast_2d(np.concatenate((screen[r, -amt:], screen[r, :-amt]))), screen[r+1:, :]), axis=0)

    return printScreen(screen)


def printScreen(screen):
    string = []
    for line in screen:
        string.append('')
        for l in line:
            string[-1] += '#' if l == 1 else ' '

    return '\n'.join(string)


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