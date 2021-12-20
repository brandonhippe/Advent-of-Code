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

    def onBorder(self, loc):
        for i in range(len(loc)):
            if loc[i] == self.mins[i] or loc[i] == self.maxs[i]:
                return True

        return False

    def inRange(self, loc):
        for i in range(len(loc)):
            if not (self.mins[i] <= loc[i] <= self.maxs[i]):
                return False

        return True

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

    def iterate(self, enhancementImg, day):
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

            if enhancementImg[enchancementIndex(self, cell, enhancementImg, day)] == '#':
                nextCells.addCell(cell)

        return nextCells

    def printCells(self):
        for i in range(self.min, self.max + 1):
            for j in range(self.min, self.max + 1):
                if self.dictString([j, i]) in self.cells:
                    print("#",end='')
                else:
                    print(".",end='')

            print("\n",end='')

        print("\n")

def enchancementIndex(imgInput, loc, enhancementImg, day):
    neighbors = imgInput.getNeighbors(loc, 1)
    index = 0
    for n in neighbors:
        index *= 2
        if imgInput.dictString(n) in imgInput.cells:
            index += 1
            continue

        if enhancementImg[0] == '#' and day % 2 == 1 and not imgInput.inRange(n):
            index += 1
            continue

    return index

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    enhancement = lines[0]
    imgInput = lines[2:]

    image = conwayCells()

    for (i, line) in enumerate(imgInput):
        for (j, l) in enumerate(line):
            if l == '#':
                image.addCell([j, i])

    for day in range(50):
        image = image.iterate(enhancement, day)

        if day == 1:
            print("\nPart 1:\nNumber of lit pixels: " + str(len(image.cells)))

    print("\nPart 2:\nNumber of lit pixels: " + str(len(image.cells)))

main()
