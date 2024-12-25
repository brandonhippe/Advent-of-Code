from collections import deque


def part1(data):
    """ 2022 Day 20 Part 1

    >>> part1(['1', '2', '-3', '3', '-2', '0', '4'])
    3
    """

    indexes = deque(range(len(data)))
    correctOrder = deque(int(line) for line in data)

    correctOrder = mix(correctOrder, indexes)[0]
    
    return getCoordinateSum(correctOrder)


def part2(data):
    """ 2022 Day 20 Part 2

    >>> part2(['1', '2', '-3', '3', '-2', '0', '4'])
    1623178306
    """

    indexes = deque(range(len(data)))
    correctOrder = deque([int(n) * 811589153 for n in data])

    for _ in range(10):
        correctOrder, indexes = mix(correctOrder, indexes)

    return getCoordinateSum(correctOrder)


def mix(correctOrder, indexes):
    for i in range(len(correctOrder)):
        loc = indexes.index(i)
        correctOrder.rotate(-loc)
        indexes.rotate(-loc)

        n = correctOrder.popleft()
        ix = indexes.popleft()

        correctOrder.rotate(-n)
        indexes.rotate(-n)

        correctOrder.appendleft(n)
        indexes.appendleft(ix)

    return [correctOrder, indexes]


def getCoordinateSum(correctOrder):
    correctOrder.rotate(-correctOrder.index(0))
    s = [correctOrder[i % len(correctOrder)] for i in [1000, 2000, 3000]]
    return sum(s)


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
        print(f"\nPart 1:\nSum of grove coordinates: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nSum of grove coordinates: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)