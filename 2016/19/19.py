import time


def main(verbose):
    data = 3014603
    part1 = int(bin(data)[3:] + bin(data)[2:3], 2)

    x = 1
    while x * 3 < data:
        x *= 3

    part2 = data - x if data <= 2 * x else x + 2 * (data - (2 * x))

    if verbose:
        print(f"\nPart 1:\nElf that steals all gifts: {part1}\n\nPart 2:\nElf that steals all gifts: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
