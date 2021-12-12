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

    def iterate(self, neighborFunction = 0, dist = 1):
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

            if numNeighbors == 3 or (numNeighbors == 2 and self.dictString(cell) in self.cells):
                nextCells.addCell(cell)

        return nextCells

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = f.readlines()

    cubes3d = conwayCells()
    cubes4d = conwayCells()
    for (i, line) in enumerate(lines):
        for (j, l) in enumerate(line):
            if l == '#':
                cubes3d.addCell([j, i, 0])
                cubes4d.addCell([j, i, 0, 0])

    for day in range(6):
        cubes3d = cubes3d.iterate()
        cubes4d = cubes4d.iterate()

    print("Part 1: " + str(len(cubes3d.cells)) + "\nPart 2: " + str(len(cubes4d.cells)))    
        
main()
