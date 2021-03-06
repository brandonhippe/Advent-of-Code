import time
import heapq
import copy

class pointOfInterest:
    def __init__(self, pos, c):
        self.pos = pos[:]
        self.id = c
        self.neighbors = []

    def genNeighbors(self, lines, others):
        openList = [[self.pos]]
        closedList = []

        while len(openList) != 0:
            path = openList.pop(0)
            pos = path[-1]

            for n in [[p + o for (p, o) in zip(pos, offset)] for offset in [[1, 0], [-1, 0], [0, 1], [0, -1]]]:
                if n in closedList or lines[n[1]][n[0]] == '#':
                    continue

                if lines[n[1]][n[0]] == '.' or lines[n[1]][n[0]] == '@' or ord('1') <= ord(lines[n[1]][n[0]])  <= ord('4'):
                    openList.append(path + [n])
                else:
                    self.neighbors.append([others[lines[n[1]][n[0]]], len(path)])

            closedList.append(pos)

class Path:
    def __init__(self, end, length):
        self.end = end
        self.length = length

def deadEndFill(lines, deadEnd):
    if lines[deadEnd[1]][deadEnd[0]] != '.':
        return

    possible = []
    
    for n in [[p + o for p, o in zip(deadEnd, offset)] for offset in [[1, 0], [-1, 0], [0, 1], [0, -1]]]:
        if 0 <= n[0] < len(lines[0]) and 0 <= n[1] < len(lines):
            if lines[n[1]][n[0]] != '#':
                possible.append(n)

    if len(possible) == 1:
        lines[deadEnd[1]][deadEnd[0]] = '#'
        deadEndFill(lines, possible[0])

def genPaths(start, neededKeys):
    openList = [[start, 0]]
    closedList = []

    paths = []
    while len(openList) != 0:
        currPOI, pathLen = openList.pop(0)

        for neighbor, dist in currPOI.neighbors:
            if neighbor in closedList or neighbor.id in neededKeys.upper():
                continue

            if neighbor.id in neededKeys:
                paths.append(Path(neighbor.id, pathLen + dist))
            else:
                openList.append([neighbor, pathLen + dist])

        closedList.append(currPOI)

    return paths

def collectKeysP1(POIs, allKeys):
    openList = [[0, "".join(sorted([k for k in allKeys.keys() if k != '@'])), '@']]
    closedList = {}

    paths = {k: {} for k in allKeys.keys()}

    while len(openList) != 0:
        pathLen, neededKeys, collected = heapq.heappop(openList)
        currKey = collected[-1]

        if len(neededKeys) == 0:
            return [pathLen, collected]

        if neededKeys not in paths[currKey].keys():
            paths[currKey][neededKeys] = genPaths(POIs[currKey], neededKeys)

        for p in paths[currKey][neededKeys]:
            newPathLen = pathLen + p.length
            newNeeded = neededKeys[:].replace(p.end, '')
            newCollected = collected[:] + p.end

            if newNeeded in closedList and closedList[newNeeded] <= newPathLen:
                continue

            valid = True
            for other in openList:
                if other[0] <= newPathLen and other[1] == newNeeded and other[2][-1] == newCollected[-1]:
                    valid = False
                    break

            if valid:
                heapq.heappush(openList, [newPathLen, newNeeded, newCollected])

        closedList[neededKeys] = pathLen

    return [0, 'ERROR']

def collectKeysP2(POIs, allKeys):
    openList = [[0, "".join(sorted([k for k in allKeys.keys() if k != '@' and not (ord('1') <= ord(k) <= ord('4'))])), '', ['1', '2', '3', '4']]]
    closedList = {}

    paths = {k: {} for k in allKeys.keys()}

    while len(openList) != 0:
        pathLen, neededKeys, collected, currKeys = heapq.heappop(openList)

        if len(neededKeys) == 0:
            return [pathLen, collected]

        for (i, currKey) in enumerate(currKeys):
            if neededKeys not in paths[currKey].keys():
                paths[currKey][neededKeys] = genPaths(POIs[currKey], neededKeys)

            for p in paths[currKey][neededKeys]:
                newPathLen = pathLen + p.length
                newNeeded = neededKeys[:].replace(p.end, '')
                newCollected = collected[:] + p.end
                newCurrKeys = currKeys[:]
                newCurrKeys[i] = p.end

                if newNeeded in closedList and closedList[newNeeded] <= newPathLen:
                    continue

                valid = True
                for other in openList:
                    if other[0] <= newPathLen and other[1] == newNeeded and other[3] == newCurrKeys:
                        valid = False
                        break

                if valid:
                    heapq.heappush(openList, [newPathLen, newNeeded, newCollected, newCurrKeys])

        closedList[neededKeys] = pathLen

    return [0, 'ERROR']

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [[x for x in line.strip()] for line in f.readlines()]

    for (y, line) in enumerate(lines):
        for (x, l) in enumerate(line):
            if l == '.':
                deadEndFill(lines, [x, y])

    linesP2 = copy.deepcopy(lines)
    POIsP1 = {}
    keysP1 = {}
    POIsP2 = {}
    keysP2 = {}
    startCount = 1
    for (y, line) in enumerate(lines):
        for (x, l) in enumerate(line):
            if l == '@' or  ord('a') <= ord(l.lower()) <= ord('z'):
                POIsP1[l] = pointOfInterest([x, y], l)
                if l != '@':
                    POIsP2[l] = pointOfInterest([x, y], l)

            if l == '@' or ord('a') <= ord(l) <= ord('z'):
                keysP1[l] = [x, y]
                if l != '@':
                    keysP2[l] = [x, y]

            pos = [x, y]
            for offset in [[x1, y1] for x1 in range(-1, 2) for y1 in range(-1, 2)]:
                newPos = [p + o for p, o in zip(pos, offset)]
                try:
                    if lines[newPos[1]][newPos[0]] == '@':
                        if sum([abs(n) for n in offset]) == 2:
                            linesP2[y][x] = str(startCount)
                            keysP2[str(startCount)] = [x, y]
                            POIsP2[str(startCount)] = pointOfInterest([x, y], str(startCount))
                            startCount += 1
                        else:
                            linesP2[y][x] = '#'
                except IndexError:
                    continue

    for p in POIsP1.values():
        p.genNeighbors(lines, POIsP1)
    
    pathLen, collected = collectKeysP1(POIsP1, keysP1)
    collected = collected.replace('@', '')

    print(f"\nPart 1:\nShortest Path: {pathLen} steps\nPath: {collected}")

    for p in POIsP2.values():
        p.genNeighbors(linesP2, POIsP2)

    pathLen, collected = collectKeysP2(POIsP2, keysP2)

    print(f"\nPart 2:\nShortest Path: {pathLen} steps\nPath: {collected}")

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
