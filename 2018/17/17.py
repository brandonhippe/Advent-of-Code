import time
import re

def expand(clay, water, start, dir):
    total = 0
    x, y = start
    settled = []
    while (x, y) not in clay:
        total += 1
        if not ((x, y + 1) in clay or ((x, y + 1) in water and water[(x, y + 1)])):
            total += flood(clay, water, (x, y))
            if not water[(x, y + 1)]:
                return [False, settled, total]
        
        settled.append((x, y))
        water[(x, y)] = True

        x += dir * 1

    return [True, settled, total]

def flood(clay, water, spring):
    total = 0
    lowest = max(c[1] for c in clay)
    
    y = spring[1]
    while (spring[0], y) not in clay and not (spring[0], y) in water and y <= lowest:
        water[(spring[0], y)] = False
        y += 1
        total += 1

    y -= 1
    total -= 1

    if y == lowest or ((spring[0], y + 1) in water and not water[(spring[0], y + 1)]):
        if y == lowest:
            total -= 1

        return total

    while y > spring[1]:
        breaking = False
        layer = []
        for dir in [-1, 1]:
            settled, layer_side, visited = expand(clay, water, (spring[0] + (dir * 1), y), dir)

            total += visited
            layer += layer_side
            if not settled:
                breaking = True

        if breaking:
            for p in layer:
                water[p] = False

            break

        water[spring[0], y] = True
        y -= 1

    return total

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    clay = set()
    for line in lines:
        xText = re.findall('x=\d+\.*\d*', line)[0][2:]
        yText = re.findall('y=\d+\.*\d*', line)[0][2:]
        
        x = [int(n) for n in re.split('\.\.', xText)]
        y = [int(n) for n in re.split('\.\.', yText)]

        if len(x) == 1:
            for i in range(y[0], y[1] + 1):
                clay.add((x[0], i))
        elif len(y) == 1:
            for i in range(x[0], x[1] + 1):
                clay.add((i, y[0]))

    water = {}
    total = flood(clay, water, (500, 0))

    print(f"\nPart 1:\nTiles reached by water: {total}")
    print(f"\nPart 2:\nWater tiles left after spring dries: {len([w for w in water.keys() if water[w]])}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
