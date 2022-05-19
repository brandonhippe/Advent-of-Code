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

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        counts = [len(re.findall(' a ', line)) for line in f.readlines()]

    print(f"\nPart 1:\nSteps to get all components on 4th floor: {steps(counts[:])}")
    print(f"\nPart 2:\nSteps to get all components on 4th floor: {steps([counts[0] + 4, *counts[1:]])}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
