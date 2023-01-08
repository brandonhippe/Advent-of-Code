import time


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
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

    part1 = count

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

    if verbose:
        print(f"\nPart 1:\nTrees hit: {part1}\n\nPart 2:\nProduct of trees hit at different slopes: {product}")

    return [part1, product]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
