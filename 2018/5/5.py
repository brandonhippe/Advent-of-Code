import time
import re

def reducePolymer(polymer):
    pattern = []
    for c in range(ord('a'), ord('z') + 1):
        pattern.append(chr(c) + chr(c).upper())
        pattern.append(chr(c).upper() + chr(c))

    pattern = f"({'|'.join(pattern)})"
    
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
