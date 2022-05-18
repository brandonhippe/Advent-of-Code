import time
import re

def validTriangle(line):
    for i in range(len(line)):
        if sum(line[:i] + line[i + 1:]) <= line[i]:
            return False

    return True

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = [[int(x) for x in re.findall('\d+', line)] for line in f.readlines()]

    print(f"\nPart 1:\nPossible triangles: {sum([1 if validTriangle(line) else 0 for line in data])}")
    
    count = 0
    for j in range(3):
        arr = []
        for i in range(len(data)):
            arr.append(data[i][j])
            if len(arr) == 3:
                count += 1 if validTriangle(arr) else 0
                arr = []

    print(f"\nPart 2:\nPossible triangles: {count}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
    