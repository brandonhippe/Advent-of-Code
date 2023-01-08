import time, sys
sys.path.insert(0,"C:/Users/Brandon Hippe/Documents/Coding Projects/Advent-of-Code/Modules")
from progressbar import printProgressBar


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    infectedP1 = set()
    infectedP2 = set()

    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if l == '#':
                infectedP1.add((x, y))
                infectedP2.add((x, y))

    pos = (len(lines[0]) // 2, len(lines) // 2)
    facing = (0, -1)
    infectedBursts = 0
    for _ in range(10_000):
        if pos in infectedP1:
            facing = (-facing[1], facing[0])
            infectedP1.remove(pos)
        else:
            facing = (facing[1], -facing[0])
            infectedP1.add(pos)
            infectedBursts += 1

        pos = tuple(p + o for p, o in zip(pos, facing))

    part1 = infectedBursts

    pos = (len(lines[0]) // 2, len(lines) // 2)
    facing = (0, -1)
    infectedBursts = 0
    weakened = set()
    flagged = set()
    for i in range(10_000_000):
        if i % (100_000) == 0 and verbose:
            printProgressBar(i + 1, 10_000_000)
            
        if pos in infectedP2:
            facing = (-facing[1], facing[0])
            infectedP2.remove(pos)
            flagged.add(pos)
        elif pos in weakened:
            weakened.remove(pos)
            infectedP2.add(pos)
            infectedBursts += 1
        elif pos in flagged:
            facing = (-facing[0], -facing[1])
            flagged.remove(pos)
        else:
            facing = (facing[1], -facing[0])
            weakened.add(pos)

        pos = tuple(p + o for p, o in zip(pos, facing))

    part2 = infectedBursts

    if verbose:
        print(f"\nPart 1:\nBursts that cause an infection: {part1}\n\nPart 2:\nBursts that cause an infection: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
