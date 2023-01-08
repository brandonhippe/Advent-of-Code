import time
from collections import deque

def main(verbose):
    data=316
    buf = deque([])

    for i in range(50_000_001):
        buf.rotate(-data)
        buf.append(i)

        if i == 2017:
            part1 = buf[0]

    part2 = buf[(buf.index(0) + 1) % len(buf)]

    if verbose:
        print(f"\nPart 1:\nNumber after 2017: {part1}\n\nPart 2:\nNumber after 50,000,000: {part2}")

    return [part1, part2]

if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
