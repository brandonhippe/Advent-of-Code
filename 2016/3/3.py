import time
import re

def validTriangle(line):
    for i in range(len(line)):
        if sum(line[:i] + line[i + 1:]) <= line[i]:
            return False

    return True

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        data = [[int(x) for x in re.findall('\d+', line)] for line in f.readlines()]

    part1 = sum([1 if validTriangle(line) else 0 for line in data])
    
    count = 0
    for j in range(3):
        arr = []
        for i in range(len(data)):
            arr.append(data[i][j])
            if len(arr) == 3:
                count += 1 if validTriangle(arr) else 0
                arr = []

    part2 = count

    if verbose:
        print(f"\nPart 1:\nPossible triangles: {part1}\n\nPart 2:\nPossible triangles: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
    