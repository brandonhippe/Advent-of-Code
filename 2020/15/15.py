import time

def main(verbose):
    data = [14, 3, 1, 0, 9, 5]
    spoken = {d: i for i, d in enumerate(data[:-1])}
    prev = data[-1]
    for i in range(len(data), 30000000):
        if i == 2020:
            part1 = prev

        if prev in spoken:
            spoken[prev], prev  = i - 1, i - 1 - spoken[prev]
        else:
            spoken[prev] = i - 1
            prev = 0

    if verbose:
        print(f"\nPart 1:\n2020th number spoken: {part1}\n\nPart 2:\n30000000th number spoken: {prev}")

    return [part1, prev]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
