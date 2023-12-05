from time import perf_counter
import re
from collections import defaultdict


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    maps = defaultdict(list)
    conversions = {}
    for line in lines[2:]:
        if len(line) == 0:
            continue

        numStrings = re.findall('\d+', line)
        if len(numStrings) == 0:
            currConv = line.split(' ')[0]
            currConv = tuple(currConv.split('-to-'))
            conversions[currConv[0]] = currConv[1]
        else:
            maps[currConv].append([int(n) for n in numStrings])

    seeds = [int(n) for n in re.findall('\d+', lines[0])]
    data = seeds[:]
    currType = 'seed'

    while currType in conversions:
        currConv = (currType, conversions[currType])

        newData = []
        for d in data:
            appended = False
            for destS, sourceS, r in maps[currConv]:
                if sourceS <= d < sourceS + r:
                    newData.append(destS + d - sourceS)
                    appended = True
                    break

            if not appended:
                newData.append(d)

        data = newData
        currType = currConv[1]

    part1 = min(data)

    part2 = float('inf')

    for i in range(0, len(seeds), 2):
        rangeS, r = seeds[i:i + 2]
        
        ranges = [[rangeS, r]]
        currType = 'seed'
        while currType in conversions:
            currConv = (currType, conversions[currType])

            newRanges = []
            while len(ranges) != 0:
                rangeS, r = ranges.pop()
                split = False
                for destS, sourceS, searchR in maps[currConv]:
                    if sourceS <= rangeS and rangeS + r <= sourceS + searchR:
                        split = True
                        newRanges.append([destS + rangeS - sourceS, r])
                        break

                    if sourceS <= rangeS < sourceS + searchR:
                        split = True
                        ranges.append([rangeS, searchR - (rangeS - sourceS)])
                        ranges.append([sourceS + searchR, r - (searchR - (rangeS - sourceS))])
                        break

                    if sourceS < rangeS + r <= sourceS + searchR:
                        split = True
                        ranges.append([rangeS, sourceS - rangeS])
                        ranges.append([sourceS, r - (sourceS - rangeS)])
                        break

                if not split:
                    newRanges.append([rangeS, r])

            currType = currConv[1]
            ranges = newRanges

        part2 = min(part2, min([r[0] for r in ranges]))

    if verbose:
        print(f"\nPart 1:\nMinimum Location Number: {part1}\n\nPart 2:\nMinimum Location Number: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
