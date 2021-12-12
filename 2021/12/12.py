class cave:
    def __init__(self, caveName):
        self.name = caveName
        self.bigCave = caveName.isupper()
        self.visited = 0
        self.links = {}

    def addLink(self, other):
        self.links[other.name] = other

def cavePathsP1(currCave):
    if currCave.name == 'end':
        return 1

    currCave.visited += 1

    possibleCaves = []
    for c in currCave.links:
        c = currCave.links[c]
        if c.bigCave or c.visited == 0:
            possibleCaves.append(c)

    count = 0
    for c in possibleCaves:
        count += cavePathsP1(c)

    currCave.visited -= 1

    return count

def cavePathsP2(currCave, smallTwice):
    if currCave.name == 'end':
        return 1

    currCave.visited += 1

    smallTwice = smallTwice or (currCave.visited == 2 and not currCave.bigCave)

    possibleCaves = []
    for c in currCave.links:
        c = currCave.links[c]
        if c.bigCave or c.visited == 0 or not smallTwice:
            possibleCaves.append(c)

    count = 0
    for c in possibleCaves:
        if c.name != 'start':
            count += cavePathsP2(c, smallTwice)

    currCave.visited -= 1

    return count


def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    caves = {}

    for line in lines:
        caveNames = line.split('-')

        for (i, name) in enumerate(caveNames):
            if not name in caves:
                caves[name] = cave(name)
        
        for (i, name) in enumerate(caveNames):
            caves[name].addLink(caves[caveNames[i - 1]])

    print("Part 1:\nNumber of paths to end cave: " + str(cavePathsP1(caves['start'])))
    print("Part 2:\nNumber of paths to end cave: " + str(cavePathsP2(caves['start'], False)))        

main()
