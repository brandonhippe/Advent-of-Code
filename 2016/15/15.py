import time
import re

class Disc:
    def __init__(self, num, positions, start):
        self.num = num
        self.numPos = positions
        self.pos = start

def fallTime(discs):
    i = 0
    while True:
        valid = True
        for disc in discs:
            if (i + disc.num + disc.pos) % disc.numPos != 0:
                valid = False
                break

        if valid:
            break

        i += 1

    return i

def main(filename):
    discs = []
    with open(filename, encoding='UTF-8') as f:
        for line in f.readlines():
            discNum, positions, _, start = [int(x) for x in re.findall('-?\d+', line)]
            discs.append(Disc(discNum, positions, start))

    print(f"\nPart 1:\nFirst time when capsule falls through: {fallTime(discs)}")
    print(f"\nPart 2:\nFirst time when capsule falls through: {fallTime(discs + [Disc(len(discs) + 1, 11, 0)])}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
