import time, sys
sys.path.insert(0,"C:/Users/Brandon Hippe/Documents/Coding Projects/Advent-of-Code/Modules")
from progressbar import printProgressBar


TILE_RULES = {'^^.', '.^^', '^..', '..^'}


def main(verbose):        
    with open("input.txt", encoding='UTF-8') as f:
        first = '.' + f.readline().strip('\n') + '.'

    safe = len([t for t in first if t == '.']) - 2
    pRow = first

    for _ in range(1, 40):
        rowText = ''
        for i in range(1, len(first) - 1):
            if pRow[i-1:i+2] in TILE_RULES:
                rowText += '^'
            else:
                rowText += '.'
                safe += 1

        pRow = '.' + rowText + '.'

    part1 = safe

    for row in range(40, 400000):
        if verbose and (row + 1) % 4000 == 0:
            printProgressBar(row + 1, 400000, decimals=0)

        rowText = ''
        for i in range(1, len(first) - 1):
            if pRow[i-1:i+2] in TILE_RULES:
                rowText += '^'
            else:
                rowText += '.'
                safe += 1

        pRow = '.' + rowText + '.'

    part2 = safe

    if verbose:
        print(f"\nPart 1:\nSafe tiles: {part1}\n\nPart 2:\nSafe tiles: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
