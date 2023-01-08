import time

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

def main(verbose):
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    orbits = {}
    for line in lines:
        line = line.split(")")
        theseOrbits = [orbits[i] if i in orbits else orbit(i) for i in line]
        theseOrbits[0].addOrbit(theseOrbits[1])

        for o in theseOrbits:
            if o.name not in orbits:
                orbits[o.name] = o

    totalOrbits = 0
    for o in orbits:
        totalOrbits += orbits[o].countOrbits()

    part2 = orbits['YOU'].orbiting.pathLen(orbits['SAN'].orbiting, orbits['YOU'])

    if verbose:
        print(f"\nPart 1:\nNumber of Direct and Indirect orbits: {totalOrbits}\n\nPart 2:\nShortest Path to Santa: {part2}")

    return [totalOrbits, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
            