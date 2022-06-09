import time
from collections import defaultdict

def findFloor(data):
    counts = defaultdict(lambda: 0)
    for d in data:
        counts[d] += 1

    return counts['('] - counts[')']

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = f.readline().strip('\n')

    print(f"\nPart 1:\nFloor Santa ends up on: {findFloor(data)}")

    for n in range(1, len(data) + 1):
        if findFloor(data[:n]) < 0:
            break

    print(f"\nPart 2:\nPosition of first character that sends Santa to the basement: {n}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
