def dictString(loc):
    string = str(loc[0])
    for l in loc[1:]:
        string += ',' + str(l)

    return string

def getNeighbors(loc):
    offsets = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i + j) % 2 == 1:
                offsets.append([i, j])

    neighbors = []
    for offset in offsets:
        neighbor = []
        for (l, o) in zip(loc, offset):
            neighbor.append(l + o)

        neighbors.append(neighbor)

    return neighbors


def heuristic(p1, p2):
    dist = 0
    for (item1, item2) in zip(p1, p2):
        dist += abs(item1 - item2)

    return dist

def aStar(data):
    riskLevels = {}
    h = {}
    g = {}
    parents = {}
    for (y, line) in enumerate(data):
        for (x, r) in enumerate(line):
            locStr = dictString([x, y])
            riskLevels[locStr] = r
            h[locStr] = heuristic([x, y], [len(data[-1]) - 1, len(data) - 1])
            g[locStr] = float('inf')

    g['0,0'] = 0

    openList = {}
    closedList = {}
    openList['0,0'] = 0

    while len(openList) != 0:
        q = ''
        minF = float('inf')
        for i in openList:
            if openList[i] < minF:
                q = i
                minF = openList[i]

        del openList[q]

        neighbors = getNeighbors([int(x) for x in q.split(',')])

        if [len(data[-1]) - 1, len(data) - 1] in neighbors:
            parents[dictString([len(data[-1]) - 1, len(data) - 1])] = q
            closedList[dictString([len(data[-1]) - 1, len(data) - 1])] = riskLevels[dictString([len(data[-1]) - 1, len(data) - 1])]
            break

        for n in neighbors:
            locStr = dictString(n)
            if not locStr in riskLevels:
                continue

            newG = g[q] + riskLevels[locStr]
            if newG < g[locStr]:
                g[locStr] = newG

            newF = g[locStr] + h[locStr]

            if locStr in openList:
                if openList[locStr] <= newF:
                    continue
            if locStr in closedList:
                if closedList[locStr] <= newF:
                    continue
            
            parents[locStr] = q
            openList[locStr] = newF
        
        closedList[q] = minF

    totalRisk = riskLevels[dictString([len(data[-1]) - 1, len(data) - 1])]
    parent = parents[dictString([len(data[-1]) - 1, len(data) - 1])]
    while parent != '0,0':
        totalRisk += riskLevels[parent]
        parent = parents[parent]

    return totalRisk

def main():
    with open('input.txt', encoding='UTF-8') as f:
        data = [[int(x) for x in line.strip()] for line in f.readlines()]

    print("\nPart 1:\nLowest Total Risk: " + str(aStar(data)))

    startLen = len(data)
    for line in data:
        if len(data) == 5 * startLen:
            break

        template = [1] * len(line)
        newLine = []
        for (l, t) in zip(line, template):
            newLine.append(l + t)

        data.append(newLine)

    for line in data:
        for l in line:
            line.append(l + 1)

            if len(line) == 5 * startLen:
                break


    for (i, line) in enumerate(data):
        for (j, r) in enumerate(line):
            data[i][j] = r % 9
            if data[i][j] == 0:
                data[i][j] = 9

    print("\nPart 2:\nLowest Total Risk: " + str(aStar(data)))

main()
