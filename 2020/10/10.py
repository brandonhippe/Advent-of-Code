import time

def adapterCombinations(data, memo):
    if len(data) == 1:
        return 1

    total = 0
    i = 1
    while i < len(data) and data[i] <= data[0] + 3:
        if tuple(data[i:]) not in memo:
            memo[tuple(data[i:])] = adapterCombinations(data[i:], memo)

        total += memo[tuple(data[i:])]
        i += 1

    return total

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        data = [0] + sorted([int(line) for line in f.readlines()])

    data.append(data[-1] + 3)

    part1 = len([1 for i in range(1, len(data)) if data[i] - data[i - 1] == 1]) * len([3 for i in range(1, len(data)) if data[i] - data[i - 1] == 3])
    part2 = adapterCombinations(data, {})

    if verbose:
        print(f"\nPart 1:\nDifferences of 1 * Differences of 3: {part1}\n\nPart 2:\nNumber of ways to arrange adapters: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
