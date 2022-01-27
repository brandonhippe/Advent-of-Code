import math
import time

class asteroid:
    def __init__(self, locArr):
        self.locArr = locArr[:]
        self.locStr = arrToStr(locArr)
        self.sees = {}
        self.bearing = 0

    def findVisible(self, asteroids):
        others = {}
        for o in asteroids:
            if o != self:
                others[o.locStr] = o

        for other in others:
            if other in self.sees:
                continue

            o = others[other]

            slope = getSlope(self, o)

            point = self.locArr[:]
            for (i, (item1, item2)) in enumerate(zip(point, slope)):
                point[i] = item1 + item2

            visible = True
            while True:
                rounded = [round(x) for x in point]
                if max([abs(item1 - item2) for (item1, item2) in zip(point, rounded)]) < 0.0001:
                    if arrToStr(rounded) == o.locStr:
                        break

                    if arrToStr(rounded) in others:
                        visible = False
                        break

                for (i, (item1, item2)) in enumerate(zip(point, slope)):
                    point[i] = item1 + item2

            if visible:
                self.sees[o.locStr] = o
                o.sees[self.locStr] = self

    def findBearing(self, station):
        self.bearing = math.atan2(self.locArr[0] - station.locArr[0], self.locArr[1] - station.locArr[1])

def getSlope(a1, a2):
    slope = [a2.locArr[0] - a1.locArr[0], a2.locArr[1] - a1.locArr[1]]

    if 1 not in slope:
        if slope[0] == 0:
            slope[1] /= abs(slope[1])
        else:
            div = abs(slope[0])
            for i in range(2):
                slope[i] /= div

    return slope

def arrToStr(arr):
    string = str(arr[0])
    for a in arr[1:]:
        string += ',' + str(a)

    return string

def strToArr(string):
    return [int(x) for x in string.split(',')]

def visibleSort(a):
    return len(a.sees)

def bearingSort(a):
    return a.bearing

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    asteroids = []
    for (y, line) in enumerate(lines):
        for (x, c) in enumerate(line):
            if c == '.':
                continue

            asteroids.append(asteroid([x,y]))

    for a in asteroids:
        a.findVisible(asteroids)

    asteroids.sort(key=visibleSort)
    print(f"\nPart 1:\nBest station location: [{asteroids[-1].locStr}] sees {len(asteroids[-1].sees)}")

    station = asteroids.pop(-1)
    removed = []
    while len(removed) + len(station.sees) < 200:
        for r in station.sees:
            a = station.sees[r]
            removed.append(asteroids.pop(asteroids.index(a)))

        station.sees = {}
        station.findVisible(asteroids)

    finalIndex = 199 - len(removed)
    removed = []
    for r in station.sees:
        a = station.sees[r]
        a.findBearing(station)
        removed.append(asteroids.pop(asteroids.index(a)))

    removed.sort(key=bearingSort)
    removed.reverse()
    print(f"\nPart 2:\n200th Asteroid Vaporized: {100 * removed[finalIndex].locArr[0] + removed[finalIndex].locArr[1]}")

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
