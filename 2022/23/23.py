from time import perf_counter
from collections import defaultdict


def printElves(mins, maxs, elves):
    for y in range(mins[1], maxs[1] + 1):
        for x in range(mins[0], maxs[0] + 1):
            if (x, y) in elves:
                print('#', end='')
            else:
                print('.', end='')

        print('')

    print('')

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    elves = set()

    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if l == '#':
                elves.add((x, y))

    MOVE_ORDER = [[[[-1, -1], [0, -1], [1, -1]], [0, -1]], [[[-1, 1], [0, 1], [1, 1]], [0, 1]], [[[-1, -1], [-1, 0], [-1, 1]], [-1, 0]], [[[1, -1], [1, 0], [1, 1]], [1, 0]]]

    round = 1
    moved = True
    while moved:
        if verbose:
            print(f"{round = }")
            
        proposed = defaultdict(set)
        moved = False
        for elf in elves:
            if all([tuple(p + o for p, o in zip(elf, offset)) not in elves for offset in [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]]):
                    continue

            moved = True

            for checks, move in MOVE_ORDER:
                if any([tuple(p + o for p, o in zip(elf, offset)) in elves for offset in checks]):
                    continue

                proposed[tuple(p + o for p, o in zip(elf, move))].add(elf)
                break

        for elf, pickedBy in zip(proposed.keys(), proposed.values()):
            if len(pickedBy) == 1:
                elves = elves.difference(pickedBy)
                elves.add(elf)

        MOVE_ORDER.append(MOVE_ORDER.pop(0))

        if round == 10:
            mins = [min(e[i] for e in elves) for i in range(2)]
            maxs = [max(e[i] for e in elves) for i in range(2)]
            part1 = (maxs[0] - mins[0] + 1) * (maxs[1] - mins[1] + 1) - len(elves)

        round += 1
    
    part2 = round - 1

    if verbose:
        print(f"\nPart 1:\n{part1}\n\nPart2:\n{part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")