import time
import re
from collections import defaultdict

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    onLights = set()
    for line in data:
        lowX, lowY, highX, highY = [int(x) for x in re.findall('\d+', line)]
        for y in range(lowY, highY + 1):
            for x in range(lowX, highX + 1):
                if (x, y) in onLights:
                    if 'off' in line or 'toggle' in line:
                        onLights.remove((x, y))
                else:
                    if 'on' in line or 'toggle' in line:
                        onLights.add((x, y))

    part1 = len(onLights)

    onLights = defaultdict(lambda: 0)
    for line in data:
        lowX, lowY, highX, highY = [int(x) for x in re.findall('\d+', line)]
        for y in range(lowY, highY + 1):
            for x in range(lowX, highX + 1):
                if 'on' in line:
                    onLights[(x, y)] += 1
                elif 'off' in line:
                    onLights[(x, y)] -= 1
                else:
                    onLights[(x, y)] += 2

                if onLights[(x, y)] < 0:
                    onLights[(x, y)] = 0

    part2 = sum(onLights.values())

    if verbose:
        print(f"\nPart 1:\nNumber of lights lit: {part1}\n\nPart 2:\nTotal brightness: {part2}")

    return [part1, part2]

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
