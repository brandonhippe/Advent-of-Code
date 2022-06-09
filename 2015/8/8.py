import time
import re

def stringChars(line):
    i = 0
    total = 0
    while i < len(line):
        if line[i] == '\\':
            if line[i + 1] == 'x':
                i += 3
            else:
                i += 1
        elif line[i] == '"':
            total -= 1

        total += 1
        i += 1

    return total

def encodedChars(line):
    total = 2
    for l in line:
        total += 1
        if l in '\\"':
            total += 1

    return total

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    print(f"\nPart 1:\nCharacters of code minus characters in strings: {sum([len(line) for line in lines]) - sum([stringChars(line) for line in lines])}")
    print(f"\nPart 2:\nCharacters of encoded minus characters in code: {sum([encodedChars(line) for line in lines]) - sum([len(line) for line in lines])}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
