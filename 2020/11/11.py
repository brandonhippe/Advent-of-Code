import time
from copy import deepcopy
from collections import defaultdict

def iterateP1(currSeats, seats):
    newSeats = set()

    for x, y in list(seats):
        neighbors = len([1 for xOff, yOff in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]] if (x + xOff, y + yOff) in currSeats])

        if ((x, y) not in currSeats and neighbors == 0) or ((x, y) in currSeats and neighbors < 4):
            newSeats.add((x, y))

    return newSeats

def iterateP2(seats, neighbors):
    newSeats = set()

    for (x, y), ns in zip(neighbors.keys(), neighbors.values()):
        nCount = len([1 for nX, nY in ns if (nX, nY) in seats])

        if ((x, y) not in seats and nCount == 0) or ((x, y) in seats and nCount < 5):
            newSeats.add((x, y))

    return newSeats

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    seats = set()
    for y, line in enumerate(data):
        for x, l in enumerate(line):
            if l != '.':
                seats.add((x, y))

    currSeats = set()
    previous = seats
    while previous != currSeats:
        previous = deepcopy(currSeats)
        currSeats = iterateP1(currSeats, seats)

    print(f"\nPart 1:\nNumber of seats occupied after settling: {len(currSeats)}")

    neighbors = defaultdict(lambda: [])
    for x, y in list(seats):
        for yOff in range(-1, 2):
            for xOff in range(-1, 2):
                if xOff == 0 and yOff == 0:
                    continue
                
                currX, currY = x + xOff, y + yOff
                while 0 <= currX < len(data[0]) and 0 <= currY < len(data[0]) and (currX, currY) not in seats:
                    currX += xOff
                    currY += yOff

                if (currX, currY) in seats:
                    neighbors[(x, y)].append((currX, currY))

    currSeats = set()
    previous = seats
    while previous != currSeats:
        previous = deepcopy(currSeats)
        currSeats = iterateP2(currSeats, neighbors)

    print(f"\nPart 2:\nNumber of seats occupied after settling: {len(currSeats)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
