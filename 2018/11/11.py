import time
import numpy as np

def printLoc(loc):
    return ",".join(str(c + 1) for c in loc)

def main(serialNo=9810):
    # 9810 is puzzle input
    grid = np.fromfunction(lambda x, y: ((((((y + 1) * ((x + 1) + 10)) + serialNo) * ((x + 1) + 10)) // 100) % 10) - 5, (300, 300), dtype=int)

    overallMax = float('-inf')
    increased = []
    for sz in range(3, 301):
        increased.append(False)
        squares = sum([grid[x:x - sz + 1 or None, y:y - sz + 1 or None] for x in range(sz) for y in range(sz)])
        maxPower = squares.max()
        location = np.concatenate(np.where(squares == maxPower))
        if sz == 3:
            print(f"\nPart 1:\nLocation of maximum power: {printLoc(location)}")
            
        if maxPower > overallMax:
            overallMax = maxPower
            loc = np.concatenate((location, np.full(1, sz - 1)))
            increased[-1] = True

        if True not in increased[-3:]:
            break

    print(f"\nPart 2:\nLocation of maximum power: {printLoc(loc)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
