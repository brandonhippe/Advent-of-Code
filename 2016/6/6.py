import time
from collections import defaultdict

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    commonP1 = ''
    commonP2 = ''
    for i in range(len(lines[0])):
        occurs = defaultdict(lambda: 0)
        for line in lines:
            occurs[line[i]] += 1

        commonP1 += list(occurs.keys())[list(occurs.values()).index(max(occurs.values()))]
        commonP2 += list(occurs.keys())[list(occurs.values()).index(min(occurs.values()))]

    print(f"\nPart 1:\nString composed of most common positional characters: {commonP1}")
    print(f"\nPart 2:\nString composed of most common positional characters: {commonP2}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
