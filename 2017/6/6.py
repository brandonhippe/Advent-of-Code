import time
import re

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        banks = [int(x) for x in re.findall('\d+', f.readline())]

    observed = set()
    steps = 0
    while tuple(banks) not in observed:
        observed.add(tuple(banks))

        moving = max(banks)
        ix = banks.index(moving)
        banks[ix] = 0

        while moving > 0:
            ix += 1
            ix %= len(banks)
            banks[ix] += 1
            moving -= 1

        steps += 1

    print(f"\nPart 1:\nRedistribution cycles before repeat: {steps}")

    steps = 0
    observedRepeat = banks[:]
    while steps == 0 or observedRepeat != banks:
        moving = max(banks)
        ix = banks.index(moving)
        banks[ix] = 0

        while moving > 0:
            ix += 1
            ix %= len(banks)
            banks[ix] += 1
            moving -= 1

        steps += 1

    print(f"\nPart 2:\nLength of loop: {steps}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
