import time
from collections import defaultdict
import re

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    bots = defaultdict(lambda: [])

    ranLines = [False] * len(lines)
    while False in ranLines:
        for i, line in enumerate(lines):
            if ranLines[i]:
                continue

            line = line.split(' ')
            vals = []
            for l in line:
                if re.search('\d+', l):
                    vals.append(int(l))

            if len(vals) == 2:
                bots[f'bot {vals[1]}'].append(vals[0])
                bots[f'bot {vals[1]}'].sort()
                ranLines[i] = True
            elif len(bots[f'bot {vals[0]}']) == 2:
                if bots[f'bot {vals[0]}'] == [17, 61]:
                    part1 = vals[0]

                for pi, b in zip([5, 10], vals[1:]):
                    bots[f'{line[pi]} {b}'].append(bots[f'bot {vals[0]}'].pop(0))
                    bots[f'{line[pi]} {b}'].sort()

                ranLines[i] = True

    part2 = bots['output 0'][0] * bots['output 1'][0] * bots['output 2'][0]

    if verbose:
        print(f"\nPart 1:\nBot that compares value 17 and 61 microchips: {part1}\n\nPart 2:\nProduct of outputs 0-2: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
