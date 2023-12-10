from time import perf_counter
from math import ceil


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    pipes = {}
    tiles = set()
    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if l == '|':
                pipes[(x, y)] = [(x, y - 1), (x, y + 1)]
            elif l == '-':
                pipes[(x, y)] = [(x - 1, y), (x + 1, y)]
            elif l == 'L':
                pipes[(x, y)] = [(x, y - 1), (x + 1, y)]
            elif l == 'J':
                pipes[(x, y)] = [(x, y - 1), (x - 1, y)]
            elif l == '7':
                pipes[(x, y)] = [(x, y + 1), (x - 1, y)]
            elif l == 'F':
                pipes[(x, y)] = [(x, y + 1), (x + 1, y)]
            elif l == 'S':
                animal = (x, y)
            else:
                tiles.add((x, y))

    pipes[animal] = []
    for pos, connects in pipes.items():
        if animal in connects and pos not in pipes[animal]:
            pipes[animal].append(pos)

    pos = animal
    loop = set()

    while pos not in loop:
        loop.add(pos)
        pos = pipes[pos][0] if pipes[pos][0] not in loop else pipes[pos][1]

    part1 = ceil(len(loop) / 2)

    part2 = 0
    for y, line in enumerate(lines):
        inside = 0
        sides = {-1: False, 1: False}
        for x, l in enumerate(line):
            if (x, y) in loop:
                for k in sides.keys():
                    if (x, y + k) in pipes[(x, y)]:
                        sides[k] = ~sides[k]
            else:
                part2 += inside

            if all(sides.values()):
                if inside == 0:
                    inside = 1
                else:
                    inside = 0

                sides = {-1: False, 1: False}

    if verbose:
        print(f"\nPart 1:\nDistance to furthest point on loop: {part1}\n\nPart 2:\nTiles enclosed by loop: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
