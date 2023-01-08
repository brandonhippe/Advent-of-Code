import time
import re

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        scanners = {}
        for line in f.readlines():
            k, v = re.findall('\d+', line)
            scanners[int(k)] = int(v)

    i = 0
    part1 = 0
    finished = False
    while not finished:
        finished = True
        for scanner, depth in zip(scanners.keys(), scanners.values()):
            if (i + scanner) % (2 * (depth - 1)) == 0:
                finished = False
                if i == 0:
                    part1 += scanner * depth
                else:
                    break

        i += 1

    if verbose:
        print(f"\nPart 1:\nTrip severity: {part1}\n\nPart 2:\nDelay in picoseconds: {i - 1}")

    return [part1, i - 1]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
