import time
from collections import defaultdict

def iterate(tiles):
    newTiles = defaultdict(lambda: 0)
    for t in list(tiles):
        for nOff in [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]:
            newTiles[tuple(p + o for p, o in zip(t, nOff))] += 1

    return set(k for k, v in zip(newTiles.keys(), newTiles.values()) if v == 2 or (k in tiles and v == 1))

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    floorTiles = set()

    for line in data:
        loc = (0, 0)
        pChar = 'e'
        for l in line:
            if l == 'e':
                if pChar != 's':
                    loc = (loc[0] + 1, loc[1])
            elif l == 'w':
                if pChar != 'n':
                    loc = (loc[0] - 1, loc[1])
            elif l == 'n':
                loc = (loc[0], loc[1] - 1)
            elif l == 's':
                loc = (loc[0], loc[1] + 1)
            
            pChar = l
        
        if loc in floorTiles:
            floorTiles.remove(loc)
        else:
            floorTiles.add(loc)
    
    print(f"\nPart 1:\nNumber of tiles with black side up: {len(floorTiles)}")

    for _ in range(100):
        floorTiles = iterate(floorTiles)

    print(f"\nPart 2:\nNumber of tiles with black side up after 100 days: {len(floorTiles)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
