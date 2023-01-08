import time, sys
sys.path.insert(0,"C:/Users/Brandon Hippe/Documents/Coding Projects/Advent-of-Code/Modules")
from progressbar import printProgressBar

def main(verbose):
    genA = 699
    genB = 124 
    aMult, bMult = 16807, 48271
    
    a, b = genA, genB
    count = 0
    for i in range(40_000_000):
        if i % (400000) == 0 and verbose:
            printProgressBar(i + 1, 40_000_000)

        a = (a * aMult) % 2147483647
        b = (b * bMult) % 2147483647

        count += 1 if a % (1 << 16) == b % (1 << 16) else 0

    part1 = count

    a, b = genA, genB
    count = 0
    for i in range(5_000_000):
        if i % (50000) == 0 and verbose:
            printProgressBar(i + 1, 5_000_000)

        while True:
            a = (a * aMult) % 2147483647

            if a % 4 == 0:
                break

        while True:
            b = (b * bMult) % 2147483647

            if b % 8 == 0:
                break

        count += 1 if a % (1 << 16) == b % (1 << 16) else 0

    if verbose:
        print(f"\nPart 1:\nMatches for 40 million pairs: {part1}\n\nPart 2:\nMatches for 5 million pairs: {count}")

    return [part1, count]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
