import time
import re

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        t = int(f.readline())
        buses = {int(x): i for i, x in enumerate(re.split(',', f.readline())) if x != 'x'}

    t1 = t
    while not any([t1 % b == 0 for b in buses.keys()]):
        t1 += 1

    part1 = (t1 - t) * ([b for b in buses.keys() if t1 % b == 0][0])

    t = 0
    step = 1
    while len(buses) > 0:
        for b in list(buses.keys())[::-1]:
            if (t + buses[b]) % b == 0:
                step *= b
                del buses[b]

        t += step

    if verbose:
        print(f"\nPart 1:\nShortest time to wait for bus multiplied by bus ID: {part1}\n\nPart 2:\nEarliest time step where buses depart at their offsets: {t - step}")

    return [part1, t - step]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
