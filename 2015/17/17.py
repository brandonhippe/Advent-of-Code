import time

def makeSize_memo(containers, s, memo):
    if s == 0:
        return [set()]

    allWays = set()
    for c in containers:
        if c <= s:
            if s - c not in memo:
                memo[s - c] = makeSize_memo(containers, s - c, memo)

            if memo[s - c] is not None:
                allWays = allWays.union({tuple(sorted(list(w) + [c], reverse=True)) for w in memo[s - c]})

    return allWays if len(allWays) != 0 else None

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        containers = tuple(sorted([int(line) for line in f.readlines()], reverse=True))

    containerCounts = {c: len([c1 for c1 in containers if c1 == c]) for c in containers}
    possibleWays = makeSize_memo(containers, 150, {})

    totalWays = 0
    smallest = float('inf')
    for pos in possibleWays:
        counts = {c: len([c1 for c1 in pos if c1 == c]) for c in pos}
        valid = True
        for c, count in zip(counts.keys(), counts.values()):
            if count > containerCounts[c]:
                valid = False
                break

        if valid:
            additional = 1
            for c in pos:
                if counts[c] == 1 and containerCounts[c] == 2:
                    additional *= 2

            totalWays += additional
            if len(pos) < smallest:
                smallest = len(pos)
                smallestWays = additional
            elif len(pos) == smallest:
                smallestWays += additional

    print(f"\nPart 1:\nCombinations of containers that can hold exactly 150 liters: {totalWays}")
    print(f"\nPart 2:\nCombinations of fewest containers that can hold exactly 150 liters: {smallestWays}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
