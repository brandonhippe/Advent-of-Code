import re


def part1(data):
    """ 2017 Day 24 Part 1

    >>> part1(['0/2', '2/2', '2/3', '3/4', '3/5', '0/1', '10/1', '9/10'])
    31
    """

    return strongest(tuple(Component([int(x) for x in re.findall('\d+', line)]) for line in data), 0, 0)[0]


def part2(data):
    """ 2017 Day 24 Part 2

    >>> part2(['0/2', '2/2', '2/3', '3/4', '3/5', '0/1', '10/1', '9/10'])
    19
    """

    return strongest(tuple(Component([int(x) for x in re.findall('\d+', line)]) for line in data), 0, 0)[-1]


class Component:
    def __init__(self, ports):
        self.ports = ports


def strongest(components, start, length):
    best = start
    longest = length
    longestStrength = start
    for i in range(len(components)):
        if start in components[i].ports:
            currPorts = components[i].ports[:]
            currPorts.pop(currPorts.index(start))
            strength, long, longStrength = strongest(components[:i] + components[i + 1:], currPorts[0], length + 1)
            strength += 2 * start
            longStrength += 2 * start
            if strength > best:
                best = strength

            if long > longest or (long == longest and longStrength > longestStrength):
                longestStrength = longStrength
                longest = long

    return [best, longest, longestStrength]


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
        print(f"\nPart 1:\nStrongest Bridge: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nStrength of longest bridge: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)