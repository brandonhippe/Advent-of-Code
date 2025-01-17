def part1(data):
    """ 2020 Day 3 Part 1

    >>> part1(['..##.......', '#...#...#..', '.#....#..#.', '..#.#...#.#', '.#...##..#.', '..#.##.....', '.#.#.#....#', '.#........#', '#.##...#...', '#...##....#', '.#..#...#.#'])
    7
    """

    x, y = 0, 0
    dx, dy = 3, 1

    count = 0
    while y < len(data):
        if data[y][x] == '#':
            count += 1

        x += dx
        x %= len(data[0])
        y += dy

    return count


def part2(data):
    """ 2020 Day 3 Part 2

    >>> part2(['..##.......', '#...#...#..', '.#....#..#.', '..#.#...#.#', '.#...##..#.', '..#.##.....', '.#.#.#....#', '.#........#', '#.##...#...', '#...##....#', '.#..#...#.#'])
    336
    """

    product = part1(data)
    for dx, dy in [(1, 1), (5, 1), (7, 1), (1, 2)]:
        x, y = 0, 0

        count = 0
        while y < len(data):
            if data[y][x] == '#':
                count += 1

            x += dx
            x %= len(data[0])
            y += dy

        product *= count

    return product


def main(verbose = False):
    from pathlib import Path
    import sys, re
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from Modules.timer import Timer
    year, day = re.findall('\d+', str(__file__))[-2:]
    
    with open(Path(__file__).parent.parent.parent / f"Inputs/{year}_{day}.txt", encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    with Timer() as p1_time:
        p1 = part1(data)

    if verbose:
        print(f"\nPart 1:\nTrees hit: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nProduct of trees hit at different slopes: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)