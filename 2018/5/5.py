import time
import re

def reducePolymer(polymer):
    pattern = '(' + '|'.join([chr(c) + chr(c).upper() for c in range(ord('a'), ord('z') + 1)]) + '|' + '|'.join([chr(c) + chr(c).lower() for c in range(ord('A'), ord('Z') + 1)]) + ')'
    pPolymer = ''
    while pPolymer != polymer:
        pPolymer = polymer[:]

        polymer = re.sub(pattern, '', polymer)

    return polymer

def main():
    with open("input.txt", encoding='UTF-8') as f:
        polymer = f.readline().strip('\n')

    print(f"\nPart 1:\nLength of reduced polymer: {len(reducePolymer(polymer))}")

    shortest = float('inf')
    for c in range(ord('a'), ord('z') + 1):
        pattern = f"({chr(c)}|{chr(c).upper()})"
        tempPolymer = re.sub(pattern, '', polymer)
        length = len(reducePolymer(tempPolymer))
        if length < shortest:
            shortest = length

    print(f"\nPart 2\nLength of shortest reduced polyemer: {shortest}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time}")
