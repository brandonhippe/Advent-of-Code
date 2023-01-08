import time
from collections import Counter

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    twos = 0
    threes = 0
    for line in lines:
        letters = Counter(line)
        twos += 1 if 2 in letters.values() else 0
        threes += 1 if 3 in letters.values() else 0

    common = ''
    for i, l1 in enumerate(lines[:-1]):
        for _, l2 in enumerate(lines[i + 1:]):
            diffCount = 0
            for c1, c2 in zip(l1, l2):
                if c1 != c2:
                    diffCount += 1

            if diffCount == 1:
                for c1, c2 in zip(l1, l2):
                    common += c1 if c1 == c2 else ''
                break

        if len(common) != 0:
            break

    if verbose:
        print(f"\nPart 1:\nChecksum: {twos * threes}\n\nPart 2:\nCommon letters between box IDs: {common}")

    return [twos * threes, common]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
