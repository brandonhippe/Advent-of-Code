import time

def main(genA=699, genB=124, printing= False):
    aMult, bMult = 16807, 48271
    
    a, b = genA, genB
    count = 0
    for i in range(40_000_000):
        if i % (400_000) == 0 and printing:
            print(f"{i // 400_000}% finished")

        a = (a * aMult) % 2147483647
        b = (b * bMult) % 2147483647

        count += 1 if a % (1 << 16) == b % (1 << 16) else 0

    print(f"\nPart 1:\nMatches for 40 million pairs: {count}")

    a, b = genA, genB
    count = 0
    for i in range(5_000_000):
        if i % (50_000) == 0 and printing:
            print(f"{i // 50_000}% finished")

        while True:
            a = (a * aMult) % 2147483647

            if a % 4 == 0:
                break

        while True:
            b = (b * bMult) % 2147483647

            if b % 8 == 0:
                break

        count += 1 if a % (1 << 16) == b % (1 << 16) else 0

    print(f"\nPart 2:\nMatches for 5 million pairs: {count}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
