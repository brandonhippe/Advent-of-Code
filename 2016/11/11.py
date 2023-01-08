import time
import re

def steps(counts):
    steps = 0
    while counts[-1] != sum(counts):
        for i, n in enumerate(counts):
            if n != 0:
                counts[i] = 0
                counts[i + 1] += n
                steps += 2 * (n-1) - 1
                break
    
    return steps

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        counts = [len(re.findall(' a ', line)) for line in f.readlines()]

    part1 = steps(counts[:])
    part2 = steps([counts[0] + 4, *counts[1:]])

    if verbose:
        print(f"\nPart 1:\nSteps to get all components on 4th floor: {part1}\n\nPart 2:\nSteps to get all components on 4th floor: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
