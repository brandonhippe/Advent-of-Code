from time import perf_counter
from collections import defaultdict


ROCKS = [[(2, 4), (3, 4), (4, 4), (5, 4)], [(2, 5), (3, 4), (3, 5), (3, 6), (4, 5)], [(2, 4), (3, 4), (4, 4), (4, 5), (4, 6)], [(2, 4), (2, 5), (2, 6), (2, 7)], [(2, 4), (2, 5), (3, 4), (3, 5)]]


def main(filename):
    with open(filename, encoding="UTF-8") as f:
        data = [-1 if c == '<' else 1 for c in f.read().strip('\n')]

    rockCount = 0
    rockIx = 0
    jetIx = 0
    rockPos = set((n, 0) for n in range(7))
    maxY = 0

    cycles = defaultdict(lambda: [])

    while True:
        if rockCount == 2022:
            print(f"\nPart 1:\n{maxY}")
        
        newRock = [tuple(p + o for p, o in zip(pos, [0, maxY])) for pos in ROCKS[rockIx]]
        pRock = newRock[:]

        cycles[(rockIx, jetIx)].append([rockCount, maxY])

        if len(cycles[(rockIx, jetIx)]) >= 3 and cycles[(rockIx, jetIx)][-1][1] - cycles[(rockIx, jetIx)][-2][1] == cycles[(rockIx, jetIx)][-2][1] - cycles[(rockIx, jetIx)][-3][1]:
            cycleLen = cycles[(rockIx, jetIx)][-1][0] - cycles[(rockIx, jetIx)][-2][0]
            heightCycle = cycles[(rockIx, jetIx)][-1][1] - cycles[(rockIx, jetIx)][-2][1]

            if (1000000000000 - rockCount) % cycleLen == 0:
                maxY += (1000000000000 - rockCount) // cycleLen * heightCycle
                break

        while not any(pos in rockPos for pos in newRock):            
            if (min(p[0] for p in newRock) > 0 and data[jetIx] == -1) or (max(p[0] for p in newRock) < 6 and data[jetIx] == 1):
                pRock = newRock[:]
                newRock = [tuple(p + o for p, o in zip(pos, [data[jetIx], 0])) for pos in newRock]

                if any(pos in rockPos for pos in newRock):
                    newRock = pRock

            jetIx += 1
            jetIx %= len(data)

            pRock = newRock[:]
            newRock = [tuple(p + o for p, o in zip(pos, [0, -1])) for pos in newRock]

        rockPos = rockPos.union(set(pRock))
        maxY = max(maxY, max(p[1] for p in pRock))

        rockIx += 1
        rockIx %= len(ROCKS)
        rockCount += 1


    print(f"\nPart 2:\n{maxY}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input.txt")
    print(f"\nRan in {perf_counter() - init_time} seconds.")