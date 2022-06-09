import time
from itertools import combinations

def prod(weights):
    total = 1
    for w in weights:
        total *= w

    return total

def splitable(weights, goal):
    for i in range(1, len(weights) + 1):
        for g in combinations(weights, i):
            if sum(g) == goal:
                return True

    return False

def splitableP2(weights, goal):
    for i in range(1, len(weights) + 1):
        for g in combinations(weights, i):
            if sum(g) == goal:
                return splitable([w for w in weights if w not in g], goal)

    return False

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        weights = [int(line) for line in f.readlines()]

    lowestEntanglement = float('inf')
    for i in range(1, len(weights) + 1):
        for g in combinations(weights, i):
            if sum(g) == sum(weights) // 3 and prod(g) < lowestEntanglement and splitable([w for w in weights if w not in g], sum(weights) // 3):
                lowestEntanglement = prod(g)

        if lowestEntanglement < float('inf'):
            break

    print(f"\nPart 1:\nLowest quantum entanglement: {lowestEntanglement}")

    lowestEntanglement = float('inf')
    for i in range(1, len(weights) + 1):
        for g in combinations(weights, i):
            if sum(g) == sum(weights) // 4 and prod(g) < lowestEntanglement and splitable([w for w in weights if w not in g], sum(weights) // 4):
                lowestEntanglement = prod(g)

        if lowestEntanglement < float('inf'):
            break

    print(f"\nPart 2:\nLowest quantum entanglement: {lowestEntanglement}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
