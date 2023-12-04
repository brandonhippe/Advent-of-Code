from time import perf_counter
import re


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    symbols = {}
    for y, line in enumerate(lines):
        for s in re.finditer('[^.]', line):
            symbols[(s.span()[0], y)] = s.group()

    partNumbers = set()
    for pos, symbol in symbols.items():
        if symbol.isdigit():
            continue

        for yoff in range(-1, 2):
            for xoff in range(-1, 2):
                nPos = tuple(p + o for p, o in zip(pos, (xoff, yoff)))

                if nPos in symbols and symbols[nPos].isdigit():
                    partNumbers.add(nPos)

    partNumberLocs = {}
    while len(partNumbers) != 0:
        x, y = list(partNumbers)[0]
        while (x - 1, y) in symbols and symbols[(x - 1, y)].isdigit():
            x -= 1

        xStart = x

        toRemove = {(x, y)}
        num = symbols[(x, y)]
        while (x + 1, y) in symbols and symbols[(x + 1, y)].isdigit():
            num += symbols[(x + 1, y)]
            toRemove.add((x + 1, y))
            x += 1

        xEnd = x

        partNumberLocs[(xStart, xEnd, y)] = int(num)
        partNumbers.difference_update(toRemove)

    part1 = sum(partNumberLocs.values())
    part2 = 0
    for pos, symbol in symbols.items():
        if symbol != '*':
            continue

        adj = set()
        for yoff in range(-1, 2):
            for xoff in range(-1, 2):
                nPos = tuple(p + o for p, o in zip(pos, (xoff, yoff)))

                for xStart, xEnd, y in partNumberLocs.keys():
                    if y == nPos[1] and xStart <= nPos[0] <= xEnd:
                        adj.add((xStart, xEnd, y))

        if len(adj) == 2:
            part2 += partNumberLocs[list(adj)[0]] * partNumberLocs[list(adj)[1]]

    if verbose:
        print(f"\nPart 1:\nSum of Part Numbers: {part1}\n\nPart 2:\nSum of Gear Ratios: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
