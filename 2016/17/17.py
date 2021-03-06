import time
import heapq
import hashlib

OFFSETS = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}

def bfsP1(data):
    openList = [['', (0, 0)]]

    while len(openList) != 0:
        currPath, currPos = openList.pop(0)

        if currPos == (3, 3):
            return currPath

        for d, n in zip('UDLR', hashlib.md5(f'{data}{currPath}'.encode()).hexdigest()[:4]):
            if n not in 'bcdef':
                continue

            pos = tuple(p + o for p, o in zip(currPos, OFFSETS[d]))
            if min(pos) < 0 or max(pos) > 3:
                continue

            openList.append([currPath + d, pos])

    return -1

def bfsP2(data):
    openList = [['', (0, 0)]]
    maxPath = 0

    while len(openList) != 0:
        currPath, currPos = openList.pop(0)

        if currPos == (3, 3):
            if len(currPath) > maxPath:
                maxPath = len(currPath)

            continue

        for d, n in zip('UDLR', hashlib.md5(f'{data}{currPath}'.encode()).hexdigest()[:4]):
            if n not in 'bcdef':
                continue

            pos = tuple(p + o for p, o in zip(currPos, OFFSETS[d]))
            if min(pos) < 0 or max(pos) > 3:
                continue

            openList.append([currPath + d, pos])

    return maxPath

def main(data = "lpvhkcbi"):
    print(f"\nPart 1:\nShortest path to vault: {bfsP1(data)}")
    print(f"\nPart 2:\nLongeset path to vault: {bfsP2(data)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
