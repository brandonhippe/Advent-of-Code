import time
import re

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

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        components = [Component([int(x) for x in re.findall('\d+', line)]) for line in f.readlines()]

    strong, _, longestStrength = strongest(components, 0, 0)
    print(f"\nPart 1:\nStrongest Bridge: {strong}")
    print(f"\nPart 2:\nStrength of longest bridge: {longestStrength}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
