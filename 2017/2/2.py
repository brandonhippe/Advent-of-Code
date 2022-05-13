import time
import re

def div(line):
    for d1 in line:
        for d2 in line:
            if d1 != d2:
                if d1 % d2 == 0:
                    return d1 // d2
                if d2 % d1 == 0:
                    return d2 // d1

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = [[int(x) for x in re.findall('-?\d+', line)] for line in f.readlines()]

    print(f"\nPart 1:\nChecksum: {sum([max(line) - min(line) for line in data])}")
    print(f"\nPart 2:\nDivsum: {sum([div(line) for line in data])}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
