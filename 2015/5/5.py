import time
from collections import defaultdict

def niceP1(string):
    if 'ab' in string or 'cd' in string or 'pq' in string or 'xy' in string:
        return False

    letterPos = defaultdict(lambda: [])
    for i, l in enumerate(string):
        letterPos[l].append(i)

    if sum(len(letterPos[v]) for v in 'aeiou') < 3:
        return False

    for pos in letterPos.values():
        for i in range(len(pos) - 1):
            if pos[i + 1] == pos[i] + 1:
                return True

    return False

def niceP2(string):
    valid = False
    for i in range(len(string) - 2):
        if string[i] == string[i + 2]:
            valid = True
            break

    if not valid:
        return False

    for i in range(len(string) - 2):
        for j in range(i + 2, len(string)):
            if string[i:i + 2] == string[j:j + 2]:
                return True

    return False

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        strings = [line.strip('\n') for line in f.readlines()]

    part1 = len([s for s in strings if niceP1(s)])
    part2 = len([s for s in strings if niceP2(s)])

    if verbose:
        print(f"\nPart 1:\nNice strings: {part1}\n\nPart 2:\nNice strings: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
