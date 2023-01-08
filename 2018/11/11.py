import time
import numpy as np

def printLoc(loc):
    return ",".join(str(c + 1) for c in loc)

def main(verbose):
    serialNo = 9810
    grid = np.fromfunction(lambda x, y: ((((((y + 1) * ((x + 1) + 10)) + serialNo) * ((x + 1) + 10)) // 100) % 10) - 5, (300, 300), dtype=int)

    overallMax = float('-inf')
    increased = []
    for sz in range(3, 301):
        increased.append(False)
        squares = sum([grid[x:x - sz + 1 or None, y:y - sz + 1 or None] for x in range(sz) for y in range(sz)])
        maxPower = squares.max()
        location = np.concatenate(np.where(squares == maxPower))
        if sz == 3:
            part1 = printLoc(location)
            
        if maxPower > overallMax:
            overallMax = maxPower
            loc = np.concatenate((location, np.full(1, sz - 1)))
            increased[-1] = True

        if True not in increased[-3:]:
            break
    
    part2 = printLoc(loc)
    
    if verbose:
        print(f"\nPart 1:\nLocation of maximum power: {part1}\n\nPart 2:\nLocation of maximum power: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
