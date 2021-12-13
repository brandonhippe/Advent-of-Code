class conwayCell:
    def __init__(self, locArr, dictString):
        self.loc = locArr[:]
        self.index = dictString

class conwayCells:
    def __init__(self):
        self.cells = {}
        self.min = float('inf')
        self.max = float('-inf')
        self.mins = 0
        self.maxs = 0
        self.side = 0

    def addCell(self, loc):
        if self.mins == 0:
            self.mins = [float('inf')] * len(loc)

        if self.maxs == 0:
            self.maxs = [float('-inf')] * len(loc)
        
        for i in range(len(loc)):
            if loc[i] > self.maxs[i]:
                self.maxs[i] = loc[i]

            if loc[i] < self.mins[i]:
                self.mins[i] = loc[i]

        self.updateMinMax()

        string = self.dictString(loc)
        self.cells[string] = conwayCell(loc, string)

    def updateMinMax(self):
        for m in self.maxs:
            if m >= self.max:
                self.max = m + 1

        for m in self.mins:
            if m <= self.min:
                self.min = m - 1

        self.side = self.max - self.min + 1
    
    def dictString(self, loc):
        s = str(loc[0])
        for l in loc[1:]:
            s += ',' + str(l)

        return s      

    def getNeighbors(self, loc, dist):
        sideLen = dist * 2 + 1

        neighbors = []
        for i in range(sideLen ** len(loc)):
            temp = [-dist] * len(loc)
            num = i
            for j in range(len(loc)):
                temp[j] += num % sideLen
                num = int(num / sideLen)
            
            neighbors.append(temp)

        output = []
        for neighbor in neighbors:
            temp = []
            for (l, n) in zip(loc, neighbor):
                temp.append(l + n)

            output.append(temp)

        return output

    def countNeighbors(self, loc, neighborFunction= 0, dist= 1):
        if neighborFunction == 0:
            neighbors = self.getNeighbors(loc, dist)
        else:
            neighbors = neighborFunction(loc, dist)

        count = 0
        for n in neighbors:
            if n != loc:
                if self.dictString(n) in self.cells:
                    count += 1                    

        return count   

    def iterate(self, aliveFunction, neighborFunction = 0, dist = 1):
        dictItem = self.cells.popitem()
        dim = len(dictItem[1].loc)
        self.addCell(dictItem[1].loc)

        nextCells = conwayCells()

        for i in range(self.side ** dim):
            cell = [self.min] * dim
            num = i
            for j in range(dim):
                cell[j] += num % self.side
                num = int(num / self.side)
            
            numNeighbors = self.countNeighbors(cell, neighborFunction, dist)

            if aliveFunction(numNeighbors, self.dictString(cell) in self.cells):
                nextCells.addCell(cell)

        return nextCells

def hexNeighbors(loc, dist):
    neighbors = [[1, 0], [1, -1], [0, -1], [-1, 0], [-1, 1], [0, 1]]

    output = []
    for neighbor in neighbors:
        temp = []
        for (l, n) in zip(loc, neighbor):
            temp.append(l + n)

        output.append(temp)

    return output

def determineAlive(numNeighbors, alive):
    return numNeighbors == 2 or (numNeighbors == 1 and alive)

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line[0:-1] for line in f.readlines()]

    floorTiles = conwayCells()

    for line in lines:
        loc = [0, 0]
        pChar = 'e'
        for l in line:
            if l == 'e':
                if pChar != 's':
                    loc[0] += 1
            elif l == 'w':
                if pChar != 'n':
                    loc[0] += -1
            elif l == 'n':
                loc[1] += -1
            elif l == 's':
                loc[1] += 1
            
            pChar = l

        locStr = floorTiles.dictString(loc)
        
        if locStr in floorTiles.cells:
            del floorTiles.cells[locStr]
        else:
            floorTiles.addCell(loc)
    
    print("Part 1: " + str(len(floorTiles.cells)))

    for day in range(100):
        floorTiles = floorTiles.iterate(determineAlive, neighborFunction=hexNeighbors)

    print("Part 2: " + str(len(floorTiles.cells)))

main()
