from itertools import combinations


def part1(data):
    """ 2015 Day 24 Part 1

    >>> part1(['1', '2', '3', '4', '5', '7', '8', '9', '10', '11'])
    99
    """

    weights = [int(line) for line in data]

    lowestEntanglement = float('inf')
    for i in range(1, len(weights) + 1):
        for g in combinations(weights, i):
            if sum(g) == sum(weights) // 3 and prod(g) < lowestEntanglement and splitable([w for w in weights if w not in g], sum(weights) // 3):
                lowestEntanglement = prod(g)

        if lowestEntanglement < float('inf'):
            break

    return lowestEntanglement


def part2(data):
    """ 2015 Day 24 Part 2

    >>> part2(['1', '2', '3', '4', '5', '7', '8', '9', '10', '11'])
    44
    """

    weights = [int(line) for line in data]

    lowestEntanglement = float('inf')
    for i in range(1, len(weights) + 1):
        for g in combinations(weights, i):
            if sum(g) == sum(weights) // 4 and prod(g) < lowestEntanglement and splitable([w for w in weights if w not in g], sum(weights) // 4, True):
                lowestEntanglement = prod(g)

        if lowestEntanglement < float('inf'):
            break

    return lowestEntanglement


def prod(weights):
    total = 1
    for w in weights:
        total *= w

    return total

def splitable(weights, goal, p2 = False):
    for i in range(1, len(weights) + 1):
        for g in combinations(weights, i):
            if sum(g) == goal:
                return True if not p2 else splitable([w for w in weights if w not in g], goal)

    return False


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
        print(f"\nPart 1:\nLowest quantum entanglement: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nLowest quantum entanglement: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)