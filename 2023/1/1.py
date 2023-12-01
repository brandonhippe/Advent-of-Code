from time import perf_counter
import re

PATT = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    data = [[re.findall('\d', line)[0], re.findall('\d', line)[-1]] for line in lines]
    part1 = sum(int(''.join(d)) for d in data)

    for n, line in enumerate(lines):
        d = data[n]
        i = line.index(d[0])
        ix = [line.index(p) if p in line else float('inf') for p in PATT]

        if min(ix) < i:
            data[n][0] = f"{ix.index(min(ix)) + 1}"

        i = line[::-1].index(d[1])
        ix = [line[::-1].index(p[::-1]) if p in line else float('inf') for p in PATT]

        if min(ix) < i:
            data[n][1] = f"{ix.index(min(ix)) + 1}"

    part2 = sum(int(''.join(d)) for d in data)

    if verbose:
        print(f"\nPart 1:\nCalibration Value: {part1}\n\nPart 2:\nCalibration Value: {part2}")


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
