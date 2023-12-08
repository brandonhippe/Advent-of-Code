from time import perf_counter
import re
from collections import defaultdict
import math


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    instructions = [0 if c == 'L' else 1 for c in lines[0]]

    nodes = {}
    for line in lines[2:]:
        lineData = re.findall('\w+', line)
        nodes[lineData[0]] = lineData[1:]

    part1 = 0
    node, endNode = 'AAA', 'ZZZ'

    while node != endNode:
        node = nodes[node][instructions[part1 % len(instructions)]]
        part1 += 1

    part2 = 0

    startNodes = {n for n in nodes.keys() if n[-1] == 'A'}
    cycles = {n: defaultdict(list) for n in startNodes}
    finishes = {n: defaultdict(list) for n in startNodes}

    for n in startNodes:
        node = n
        steps = 0
        found = False

        while not found:
            if node[-1] == 'Z':
                finishes[n][node].append(steps)
                
            cycles[n][node].append(steps)
            node = nodes[node][instructions[steps % len(instructions)]]
            steps += 1

            if node in cycles[n]:
                for prev in cycles[n][node]:
                    if (steps - prev) % len(instructions) == 0:
                        cycles[n] = steps - prev
                        found = True
                        break
    
    part2 = math.lcm(*cycles.values())

    if verbose:
        print(f"\nPart 1:\n{part1}\n\nPart 2:\n{part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
