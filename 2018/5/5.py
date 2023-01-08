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

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        polymer = f.readline().strip('\n')

    part1 = len(reducePolymer(polymer))

    shortest = float('inf')
    for c in range(ord('a'), ord('z') + 1):
        pattern = f"({chr(c)}|{chr(c).upper()})"
        tempPolymer = re.sub(pattern, '', polymer)
        length = len(reducePolymer(tempPolymer))
        if length < shortest:
            shortest = length

    if verbose:
        print(f"\nPart 1:\nLength of reduced polymer: {part1}\n\nPart 2\nLength of shortest reduced polyemer: {shortest}")

    return [part1, shortest]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time}")
