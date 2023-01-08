from time import perf_counter


def main(verbose):
    with open("input.txt", encoding="UTF-8") as f:
        lines = [[int(x) for x in line.strip('\n')] for line in f.readlines()]

    visible = set()
    Y = len(lines)
    X = len(lines[0])

    for r in range(Y):
        val = lines[r][0]
        for c in range(X):
            if c == 0 or lines[r][c] > val:
                visible.add((r, c))
                val = lines[r][c]

    for r in range(Y):
        val = lines[r][-1]
        for c in reversed(range(X)):
            if c == X - 1 or lines[r][c] > val:
                visible.add((r, c))
                val = lines[r][c]

    for c in range(X):
        val = lines[0][c]
        for r in range(Y):
            if r == 0 or lines[r][c] > val:
                visible.add((r, c))
                val = lines[r][c]

    for c in range(X):
        val = lines[-1][c]
        for r in reversed(range(Y)):
            if r == X - 1 or lines[r][c] > val:
                visible.add((r, c))
                val = lines[r][c]

    part1 = len(visible)

    maxScore = 0
    for y in range(1, Y - 1):
        for x in range(1, X - 1):
            val = lines[y][x]
            score = 1

            count = 0
            for r in range(y + 1, Y):
                count += 1 if lines[r][x] < val else 0
                if lines[r][x] >= val:
                    count += 1
                    break

            score *= count

            count = 0
            for r in reversed(range(0, y)):
                count += 1 if lines[r][x] < val else 0
                if lines[r][x] >= val:
                    count += 1
                    break

            score *= count

            count = 0
            for c in range(x + 1, X):
                count += 1 if lines[y][c] < val else 0
                if lines[y][c] >= val:
                    count += 1
                    break

            score *= count

            count = 0
            for c in reversed(range(0, x)):
                count += 1 if lines[y][c] < val else 0
                if lines[y][c] >= val:
                    count += 1
                    break

            score *= count

            maxScore = max(score, maxScore)

    if verbose:
        print(f"\nPart 1:\n{part1}\n\nPart 2:\n{maxScore}")

    return [part1, maxScore]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")