from time import perf_counter
import re


def extrapolate_p1(seq):
    if len(set(seq)) == 1:
        return seq[-1]
    
    diffs = [seq[i] - seq[i - 1] for i in range(1, len(seq))]
    return seq[-1] + extrapolate_p1(diffs)


def extrapolate_p2(seq):
    if len(set(seq)) == 1:
        return seq[0]
    
    diffs = [seq[i] - seq[i - 1] for i in range(1, len(seq))]
    return seq[0] - extrapolate_p2(diffs)


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    data = [[int(n) for n in re.findall('-?\d+', line)] for line in lines]

    part1 = sum(extrapolate_p1(seq) for seq in data)
    part2 = sum(extrapolate_p2(seq) for seq in data)

    if verbose:
        print(f"\nPart 1:\n{part1}\n\nPart 2:\n{part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
