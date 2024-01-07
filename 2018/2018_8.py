import re


def part1(data):
    """ 2018 Day 8 Part 1

    >>> part1(['2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'])
    138
    """

    tree = Node()
    tree.parse([int(x) for x in re.findall('\d+', data[0])])
    return tree.metadataSum()


def part2(data):
    """ 2018 Day 8 Part 2

    >>> part2(['2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'])
    66
    """

    tree = Node()
    tree.parse([int(x) for x in re.findall('\d+', data[0])])
    return tree.evaluate()


class Node:
    def __init__(self):
        self.subNodes = []
        self.metadata = []

    def parse(self, input):
        numChildren, numData = input[:2]
        input = input[2:]

        for _ in range(numChildren):
            self.subNodes.append(Node())
            input = self.subNodes[-1].parse(input)

        self.metadata = input[:numData]
        return input[numData:]

    def metadataSum(self):
        return sum([c.metadataSum() for c in self.subNodes]) + sum(self.metadata)

    def evaluate(self):
        if len(self.subNodes) == 0:
            return sum(self.metadata)

        total = 0
        for n in self.metadata:
            i = n - 1
            if i < len(self.subNodes):
                total += self.subNodes[i].evaluate()

        return total


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
        print(f"\nPart 1:\nSum of metadata entries: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nValue of root node: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)