from time import perf_counter

def main(filename):
    with open(filename, encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    pairs = [[[int(x) for x in pairs.split('-')] for pairs in line.split(',')] for line in lines]

    overlaps = 0
    for a1, a2 in pairs[:]:
        if (min(a1) <= min(a2) and max(a1) >= max(a2)) or (min(a2) <= min(a1) and max(a2) >= max(a1)):
            overlaps += 1
                

    print(f"\nPart 1:\n{overlaps}")


    overlaps = 0
    for a1, a2 in pairs:
        if min(a1) <= min(a2) <= max(a1) or min(a1) <= max(a2) <= max(a1) or min(a2) <= min(a1) <= max(a2) or min(a2) <= max(a1) <= max(a2):
            overlaps += 1

    print(f"\nPart 2:\n{overlaps}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input.txt")
    print(f"\nRan in {perf_counter() - init_time} seconds.")
    