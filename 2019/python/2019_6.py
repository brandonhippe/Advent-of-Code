def part1(data):
    """ 2019 Day 6 Part 1

    >>> part1(['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L'])
    42
    """

    orbits = {}
    for line in data:
        line = line.split(")")
        theseOrbits = [orbits[i] if i in orbits else orbit(i) for i in line]
        theseOrbits[0].addOrbit(theseOrbits[1])

        for o in theseOrbits:
            if o.name not in orbits:
                orbits[o.name] = o

    return sum([o.countOrbits() for o in orbits.values()])


def part2(data):
    """ 2019 Day 6 Part 2

    >>> part2(['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L', 'K)YOU', 'I)SAN'])
    4
    """

    orbits = {}
    for line in data:
        line = line.split(")")
        theseOrbits = [orbits[i] if i in orbits else orbit(i) for i in line]
        theseOrbits[0].addOrbit(theseOrbits[1])

        for o in theseOrbits:
            if o.name not in orbits:
                orbits[o.name] = o

    return orbits['YOU'].orbiting.pathLen(orbits['SAN'].orbiting, orbits['YOU'])


class orbit:
    def __init__(self, name):
        self.name = name
        self.orbiting = self
        self.orbiters = []

    def addOrbit(self, other):
        self.orbiters.append(other)
        other.orbiting = self

    def countOrbits(self):
        count = 0
        for o in self.orbiters:
            count += 1 + o.countOrbits()

        return count

    def pathLen(self, goal, prev):
        if self == goal:
            return 0

        shortest = float('inf')
        for o in self.orbiters:
            if o == prev:
                continue
            
            path = o.pathLen(goal, self)
            if path < shortest:
                shortest = path

        if shortest == float('inf')and self.orbiting != prev and self.orbiting != 0:
            shortest = self.orbiting.pathLen(goal, self)

        return shortest + 1


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
        print(f"\nPart 1:\nNumber of Direct and Indirect orbits: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nShortest path to Santa: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)