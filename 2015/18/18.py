import time

def iterate(positons):
    newPositions = set()
    for y in range(100):
        for x in range(100):
            neighbors = 0
            for yOff in range(-1, 2):
                for xOff in range(-1, 2):
                    if xOff == 0 and yOff == 0:
                        continue

                    if (x + xOff, y + yOff) in positons:
                        neighbors += 1

            if ((x, y) in positons and (neighbors == 2 or neighbors == 3)) or ((x, y) not in positons and neighbors == 3):
                newPositions.add((x, y))

    return newPositions

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    positions = set()
    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if l == '#':
                positions.add((x, y))

    for _ in range(100):
        positions = iterate(positions)

    print(f"\nPart 1:\nLights on after 100 iterations: {len(positions)}")

    corners = {(0, 0), (0, 99), (99, 0), (99, 99)}
    positions = set()
    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if l == '#':
                positions.add((x, y))

    positions = positions.union(corners)

    for _ in range(100):
        positions = iterate(positions)
        positions = positions.union(corners)

    print(f"\nPart 2:\nLights on after 100 iterations with corners stuck on: {len(positions)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
