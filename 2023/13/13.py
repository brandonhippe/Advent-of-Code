from time import perf_counter


def findRefs(pattern):
    ## Find vertical reflections
    vertical = {}
    for i in range(1, len(pattern[0])):
        vertical[i] = 0
        leftCol, rightCol = i - 1, i

        while leftCol >= 0 and rightCol < len(pattern[0]):
            for row in range(len(pattern)):
                vertical[i] += pattern[row][leftCol] != pattern[row][rightCol]

            leftCol -= 1
            rightCol += 1

    ## Find horizontal reflections
    horizontal = {}
    for i in range(1, len(pattern)):
        horizontal[i] = 0
        aboveRow, belowRow = i - 1, i

        while aboveRow >= 0 and belowRow < len(pattern):
            for col in range(len(pattern[0])):
                horizontal[i] += pattern[aboveRow][col] != pattern[belowRow][col]

            aboveRow -= 1
            belowRow += 1

    return vertical, horizontal


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    lines.append('')

    part1 = 0
    part2 = 0
    pattern = []
    for line in lines:
        if len(line) == 0:
            vert, horiz = findRefs(pattern)

            for k, v in vert.items():
                if v == 0:
                    part1 += k
                if v == 1:
                    part2 += k

            for k, v in horiz.items():
                if v == 0:
                    part1 += 100 * k
                if v == 1:
                    part2 += 100 * k

            pattern = []
        else:
            pattern.append(line)

    if verbose:
        print(f"\nPart 1:\nSummary of Notes: {part1}\n\nPart 2:\nSummary after desmudging: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
