import time
import heapq

class Path:
    def __init__(self, found, pathLen):
        self.found = found[:]
        self.length = pathLen

def genPaths(lines, k1):
    neighborOffsets = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    openList = [[[k1[1]], []]]
    closedList = []

    paths = []
    while len(openList) != 0:
        path, found = openList.pop(0)
        pos = path[-1]

        for n in [[p + o for (p, o) in zip(pos, offset)] for offset in neighborOffsets]:
            if n in closedList or lines[n[1]][n[0]] == '#':
                continue

            c = lines[n[1]][n[0]]
            if ord('a') <= ord(c) <= ord('z'):
                openList.append([path + [n], found[:] + [c]])
                paths.append(Path(found[:] + [c], len(path)))
            elif ord('A') <= ord(c) <= ord('Z'):
                openList.append([path + [n], found[:] + [c]])
            else:
                openList.append([path + [n], found[:]])

        closedList.append(pos)

    return paths

def collectKeys(paths, allKeys):
    openList = [[0, ['@'], '@']]
    closedList = {}

    while len(openList) != 0:
        pathLen, sorted, collected = heapq.heappop(openList)
        currKey = collected[-1]

        if sorted == allKeys:
            return [pathLen, collected]

        for p in paths[currKey]:
            newPathLen = pathLen + p.length
            newSorted = sorted[:]
            newCollected = collected[:]

            if p.found[-1] in newCollected:
                continue
            
            valid = True
            for c in p.found:
                if ord('a') <= ord(c) <= ord('z'):
                    if c not in newCollected:
                        newSorted.append(c)
                        newCollected += c
                else:
                    if c.lower() not in newCollected:
                        valid = False
                        break
            

            if not valid:
                continue

            newSorted.sort()
            sortedString = ''
            for s in newSorted:
                sortedString += s

            if sortedString in closedList and closedList[sortedString] <= newPathLen:
                continue

            valid = True
            for other in openList:
                if other[1] == newSorted and other[0] <= newPathLen:
                    valid = False
                    break

            if valid:
                heapq.heappush(openList, [newPathLen, newSorted, newCollected])

        sortedString = ''
        for s in sorted:
            sortedString += s

        closedList[sortedString] = pathLen

    return [0, 'ERROR']

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [[x for x in line.strip()] for line in f.readlines()]

    keys = []
    doors = []
    for (y, line) in enumerate(lines):
        for (x, l) in enumerate(line):
            if l == '@':
                start = [x, y]
            elif ord('a') <= ord(l) <= ord('z'):
                keys.append([l, [x, y]])
            elif ord('A') <= ord(l) <= ord('Z'):
                doors.append([l, [x, y]])

    keys = [['@', start]] + keys
    keys.sort(key=lambda k: k[0])

    paths = {}
    for k1 in keys:
        paths[k1[0]] = genPaths(lines, k1)

    print("Found all paths between pairs of keys")

    pathLen, collected = collectKeys(paths, [k[0] for k in keys])
    collected = collected.replace('@', '')

    print(f"\nPart 1:\nShortest Path: {pathLen} steps\nPath: {collected}")

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
