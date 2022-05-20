import time

TILE_RULES = {'^^.', '.^^', '^..', '..^'}

def main(filename, progress = False):
    if progress:
        from Modules.progressbar import printProgressBar
        
    with open(filename, encoding='UTF-8') as f:
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

    print(f"\nPart 1:\nSafe tiles: {safe}")

    for row in range(40, 400000):
        if progress and (row + 1) % 4000 == 0:
            printProgressBar(row + 1, 400000, decimals=0)

        rowText = ''
        for i in range(1, len(first) - 1):
            if pRow[i-1:i+2] in TILE_RULES:
                rowText += '^'
            else:
                rowText += '.'
                safe += 1

        pRow = '.' + rowText + '.'

    print(f"\nPart 2:\nSafe tiles: {safe}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt", True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
