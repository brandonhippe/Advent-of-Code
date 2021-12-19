class vector:
    def __init__(self, v=0, vText=0):
        if v != 0:
            self.v = v[:]
            self.text = self.genText(self.v)
        elif vText != 0:
            self.text = vText
            self.v = [int(x) for x in self.text.split(',')]
    
    def genText(self, arr):
        text = str(arr[0])
        for e in arr[1:]:
            text += ',' + str(e)

        return text

    def subtract(self, other):
        diff = []
        for (s, o) in zip(self.v, other.v):
            diff.append(s - o)

        return vector(v=diff)

    def add(self, other):
        summation = []
        for (s, o) in zip(self.v, other.v):
            summation.append(s + o)

        return vector(v=summation)

    def orient(self, orientation):
        newV = self.v[:]

        if orientation < 16:
            for i in range((orientation // 4)):
                newV = self.rotateX(newV)
        if orientation >= 16:
            for i in range((orientation - 12) // 4):
                newV = self.rotateY(newV)
            
            if orientation >= 20:
                newV = self.rotateY(newV)

        for i in range(orientation % 4):
            newV = self.rotateZ(newV)

        return vector(v=newV)       

    def rotateX(self, arr):
        return [arr[0], -arr[2], arr[1]]

    def rotateY(self, arr):
        return [arr[2], arr[1], -arr[0]]

    def rotateZ(self, arr):
        return [-arr[1], arr[0], arr[2]]

class scanner:
    def __init__(self, sNum):
        self.number = sNum
        self.relBeacons = {}
        self.absBeacons = {}
        self.loc = []

        if self.number == 0:
            self.loc = vector(v=[0, 0, 0])

    def addBeacon(self, relLoc):
        self.relBeacons[relLoc] = vector(vText=relLoc)
        if self.number == 0:
            self.absBeacons[relLoc] = vector(vText=relLoc)

    def beaconDiffs(self):
        diffs = {}
        for i in self.relBeacons:
            for j in self.relBeacons:
                if i != j:
                    diffs[i + ':' + j] = self.relBeacons[j].subtract(self.relBeacons[i])

        return diffs

    def calcAbs(self):
        for i in self.relBeacons:
            self.absBeacons[i] = self.loc.add(self.relBeacons[i])

    def setOrientation(self, orientationNum):
        newRels = {}
        for i in self.relBeacons:
            newV = self.relBeacons[i].orient(orientationNum)
            newRels[newV.text] = newV

        self.relBeacons = newRels


def commonBeacons(s1, s2):
    s1Diffs = s1.beaconDiffs()
    s2Diffs = s2.beaconDiffs()
    
    common = []
    pLen = 1
    while len(common) != pLen:
        pLen = len(common)
        for i in s1Diffs:
            possible = []
            for j in s2Diffs:
                if s1Diffs[i].text == s2Diffs[j].text:
                    possible.append(j)

            if len(possible) == 1:
                points1 = i.split(":")
                points2 = possible[0].split(":")

                for (p1, p2) in zip(points1, points2):
                    newCommon = p1 + ":" + p2
                    if not newCommon in common:
                        common.append(newCommon)

                del s1Diffs[i]
                del s2Diffs[possible[0]]
                s1Del = points1[-1] + ":" + points1[0]
                if s1Del in s1Diffs:
                    del s1Diffs[s1Del]
                s2Del = points2[-1] + ":" + points2[0]
                if s2Del in s2Diffs:
                    del s2Diffs[s2Del]
                break

    return common

def assignAbs(s1, s2, common):
    if len(s1.absBeacons) != 0 and len(s2.absBeacons) == 0:
        cBeacon = common[0].split(":")
        beacon1 = [int(x) for x in cBeacon[0].split(',')]
        beacon2 = [-int(x) for x in cBeacon[1].split(',')]
        s2L = []
        for (s1L, b1, b2) in zip(s1.loc.v, beacon1, beacon2):
            s2L.append(s1L + b1 + b2)

        s2.loc = vector(v=s2L)
        s2.calcAbs()
    elif len(s2.absBeacons) != 0 and len(s1.absBeacons) == 0:
        cBeacon = common[0].split(":")
        cBeacon.reverse()
        beacon1 = [int(x) for x in cBeacon[0].split(',')]
        beacon2 = [-int(x) for x in cBeacon[1].split(',')]
        s1L = []
        for (s2L, b1, b2) in zip(s2.loc.v, beacon1, beacon2):
            s1L.append(s2L + b1 + b2)

        s1Loc = vector(v=s1L)
        s1.calcAbs()

    beacons = []
    for b in s1.absBeacons:
        beacons.append(s1.absBeacons[b].text)
    for b in s2.absBeacons:
        beacons.append(s2.absBeacons[b].text)
    
    return beacons

def manhatDist(l1, l2):
    dist = 0
    for (c1, c2) in zip(l1, l2):
        dist += abs(c1 - c2)

    return dist

def main():
    with open('input.txt',encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    beacons = []
    scanners = []
    for line in lines:
        if len(line) == 0:
            continue

        if line[-1] == '-':
            scannerNum = int(line.split("--- scanner ")[1].split(" ")[0])
            scanners.append(scanner(scannerNum))
            continue
        elif scannerNum == 0:
            beacons.append(line)
        
        scanners[-1].addBeacon(line)

    while True:
        for i in scanners:
            if len(i.absBeacons) == 0:
                continue

            for j in scanners:
                foundBeacons = []
                if len(j.absBeacons) != 0 or i == j:
                    continue
                
                tempRels = j.relBeacons

                for o in range(24):
                    j.setOrientation(o)
                    common = commonBeacons(i, j)

                    if len(common) >= 12:
                        if len(i.absBeacons) != 0 or len(j.absBeacons) != 0:
                            foundBeacons = assignAbs(i, j, common)
                            break
                    
                    j.relBeacons = tempRels

                for b in foundBeacons:
                    if b not in beacons:
                        beacons.append(b)

        checkAgain = False
        for s in scanners:
            if len(s.absBeacons) == 0:
                checkAgain = True
                break
        
        if not checkAgain:
            break

    print("\nPart 1:\nNumber of Beacons: " + str(len(beacons)))

    max = float('-inf')
    for s1 in scanners:
        for s2 in scanners:
            dist = manhatDist(s1.loc.v, s2.loc.v)
            if dist > max:
                max = dist

    print("\nPart 2:\nFarthest Apart Scanners: " + str(max))

main()
