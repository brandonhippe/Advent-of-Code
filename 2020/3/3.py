import time

from numpy import product

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    x, y = 0, 0
    dx, dy = 3, 1

    count = 0
    while y < len(lines):
        if lines[y][x] == '#':
            count += 1

        x += dx
        x %= len(lines[0])
        y += dy

    print(f"\nPart 1:\nTrees hit: {count}")

    product = count
    for dx, dy in [(1, 1), (5, 1), (7, 1), (1, 2)]:
        x, y = 0, 0

        count = 0
        while y < len(lines):
            if lines[y][x] == '#':
                count += 1

            x += dx
            x %= len(lines[0])
            y += dy

        product *= count

    print(f"\nPart 2:\nProduct of trees hit at different slopes: {product}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
