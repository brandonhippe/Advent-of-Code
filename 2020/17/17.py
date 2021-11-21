class cube:
    def __init__(self, table, coords):
        self.c = coords[:]
        self.hash = table.hash(self.c)
        table.linkedLists[self.hash].addNode(self)

    def countNeighbors(self, table):
        count = 0
        neighbors = []
        for i in range(3 ** table.dim):
            val = i
            arr = [0] * table.dim
            for j in range(table.dim):
                arr[j] = (val % 3) - 1
                val = int(val / 3)
            
            neighbors.append(arr)

        for o in neighbors:
            n = []
            for (a, b) in zip(self.c, o):
                n.append(a + b)
            
            nCube = table.search(n)
            if nCube != 0 and nCube != self:
                count += 1

        return count

class linkedList:
    def __init__(self):
        self.head = 0
    
    def addNode(self, n):
        if self.head == 0:
            self.head = n
            n.next = 0
        else:
            curr = self.head
            while curr.next != 0:
                curr = curr.next
            
            curr.next = n
            n.next = 0

    def search(self, loc):
        curr = self.head
        while curr != 0:
            if loc == curr.c:
                break
            
            curr = curr.next

        return curr

    def print(self):
        if self.head == 0:
            print("Nothing in list")
            return

        curr = self.head
        while curr != 0:
            print("Coords:", end=' ')
            print(curr.c, end=' ')
            print("State: True")

            curr = curr.next

class hashTable:
    def __init__(self, side, dim):
        self.dim = dim
        self.size = side ** self.dim
        self.maxCoord = int((side - 1) / 2.0)

        self.linkedLists = [0] * self.size
        for i in range(self.size):
            self.linkedLists[i] = linkedList()
    
    def hash(self, c):
        count = 0
        for val in c:
            count += abs(val)
        
        return count % self.size

    def search(self, c):
        h = self.hash(c)
        return self.linkedLists[h].search(c)

    def iterate(self):
        offset = self.maxCoord + 1
        base = offset * 2 + 1
        allCubes = []

        for i in range(base ** self.dim):
            val = i
            arr = [0] * self.dim
            for j in range(self.dim):
                arr[j] = (val % base) - offset
                val = int(val / base)
            
            allCubes.append(arr)

        
        aliveNext = []

        for loc in allCubes:
            c = self.search(loc)
            alive = True
            if c == 0:
                c = cube(self, loc)
                alive = False
                
            count = c.countNeighbors(self)

            if count == 3 or (alive and count == 2):
                aliveNext.append(loc)

        nextSide = base - 2
        for loc in aliveNext:
            if offset in loc or -offset in loc:
                nextSide += 2
                break

        nextStates = hashTable(nextSide, self.dim)
        for loc in aliveNext:
            cube(nextStates, loc)

        return nextStates



    def print(self):
        for (i, l) in enumerate(self.linkedLists):
            print("Hash: " + str(i) + "\nCubes:")
            l.print()
            print(" ")


def main():
    with open('input1.txt', encoding='UTF-8') as f:
        lines = f.readlines()

    finalStates = hashTable(len(lines), 3)

    for (i, line) in enumerate(lines):
        y = i - finalStates.maxCoord
        for (j, c) in enumerate(line):
            if c == '#':
                x = j - finalStates.maxCoord
                cube(finalStates, [x, y, 0])

    finalStates = finalStates.iterate()

    for i in range(-finalStates.maxCoord, finalStates.maxCoord + 1):
        for j in range(-finalStates.maxCoord, finalStates.maxCoord + 1):
            c = finalStates.search([j, i, 0])
            p = '.'
            if c != 0:
                p = '#'                    
                
            print(p, end='')
        print(" ")
    
    print("\nDone")
        
main()