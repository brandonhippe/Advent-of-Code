import time
from itertools import combinations

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = [int(x) for x in f.readlines()]

    for i, val in enumerate(data):
        if i < 25:
            continue

        if val not in [sum(c) for c in combinations(data[i - 25:i], 2)]:
            break

    print(f"\nPart 1:\nFirst value that is not the sum of two of the previous 25: {val}")

    for l in range(2, len(data)):
        found = False
        for i in range(len(data) - i - 1):
            if sum(data[i:i + l]) == val:
                found = True
                break

        if found:
            break

    print(f"\nPart 2:\nSum of largest and smallest values in contiguous string that sum to invalid number: {min(data[i:i + l]) + max(data[i:i + l])}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
