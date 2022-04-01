import time
import copy

def genRating(bugState):
    rating = 0
    for (i, c) in enumerate(bugState):
        if c == '#':
            rating += 2 ** i

    return rating

def getState(bugs):
    string = ''
    for y in range(5):
        for x in range(5):
            string += '#' if ",".join([str(x), str(y)]) in bugs else '.'

    return string

def part1(bugs):
    pastBugs = [getState(bugs)]
    while True:
        newBugs = {}

        for y in range(5):
            for x in range(5):
                neighbors = 0
                for n in genNeighbors(x, y):
                    neighbors += 1 if ",".join([str(c) for c in n[:-1]]) in bugs else 0

                if neighbors == 1 or (neighbors == 2 and ",".join([str(x), str(y)]) not in bugs):
                    newBugs[",".join([str(x), str(y)])] = 1

        bugState = getState(newBugs)
        if bugState in pastBugs:
            return genRating(bugState)
        else:
            pastBugs.append(bugState)

        bugs = newBugs

def genNeighbors(x, y, level=None):
    neighbors = []
    for n in [[-1, 0], [0, -1], [1, 0], [0, 1]]:
        nX, nY = [p + o for p, o in zip([x, y], n)]
        if level is not None:
            if not (0 <= nX < 5 and 0 <= nY < 5):
                # Outside edge, going 'up' a level
                if nX == -1:
                    neighbors.append([1, 2, level - 1])
                elif nX == 5:
                    neighbors.append([3, 2, level - 1])
                elif nY == -1:
                    neighbors.append([2, 1, level - 1])
                elif nY == 5:
                    neighbors.append([2, 3, level - 1])
            elif (nY * 5) + nX == 12:
                # Inside edge, going 'down' a level
                index = (y * 5) + x
                if index == 7:
                    for i in range(5):
                        neighbors.append([i, 0, level + 1])
                elif index == 11:
                    for i in range(5):
                        neighbors.append([0, i, level + 1])
                elif index == 13:
                    for i in range(5):
                        neighbors.append([4, i, level + 1])
                elif index == 17:
                    for i in range(5):
                        neighbors.append([i, 4, level  + 1])
            elif nX != 2 or nY != 2:
                neighbors.append([nX, nY, level])
        elif 0 <= nX < 5 and 0 <= nY < 5:
            neighbors.append([nX, nY, level])

    return neighbors

def part2(bugs):
    for _ in range(200):
        maxLevel = max([abs([int(x) for x in c.split(',')][-1]) for c in bugs.keys()]) + 1
        newBugs = {}

        for level in range(-maxLevel, maxLevel + 1):
            for y in range(5):
                for x in range(5):
                    if x == 2 and y == 2:
                        continue

                    neighbors = 0
                    for n in genNeighbors(x, y, level):
                        neighbors += 1 if ",".join([str(c) for c in n]) in bugs else 0

                    if neighbors == 1 or (neighbors == 2 and ",".join([str(x), str(y), str(level)]) not in bugs):
                        newBugs[",".join([str(x), str(y), str(level)])] = 1

        bugs = newBugs

    return len(bugs)

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [[x for x in line.strip('\n')] for line in f.readlines()]

    bugsP1 = {}
    bugsP2 = {}
    for (y, line) in enumerate(lines):
        for (x, l) in enumerate(line):
            if l == '#':
                bugsP1[",".join([str(x), str(y)])] = 1
                bugsP2[",".join([str(x), str(y), '0'])] = 1

    print(f"\nPart 1:\nBiodiversity rating for first repeated state: {part1(bugsP1)}")
    print(f"\nPart 2:\nNumber of bugs present after 200 minutes: {part2(bugsP2)}")
    
init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")