from time import perf_counter
import re


def extrapolate(seq):
    if len(set(seq)) == 1:
        return seq[-1]
    
    diffs = [seq[i] - seq[i - 1] for i in range(1, len(seq))]
    return seq[-1] + extrapolate(diffs)


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    data = [[int(n) for n in re.findall('-?\d+', line)] for line in lines]

    part1 = sum(extrapolate(seq) for seq in data)
    part2 = sum(extrapolate(seq[::-1]) for seq in data)

    if verbose:
        print(f"\nPart 1:\nExtrapolated Value: {part1}\n\nPart 2:\nReverse Extrapolated Value: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
