import time
import re
import copy

class Point:
    def __init__(self, infoLine):
        data = [int(x) for x in re.findall('[- ]?\d+', infoLine)]
        self.pos = data[:len(data)//2]
        self.vel = data[len(data)//2:]

    def applyVel(self, iterations=1):
        for i, (p, v) in enumerate(zip(self.pos, self.vel)):
            self.pos[i] = p + (v * iterations)

    def __str__(self) -> str:
        return ",".join(str(x) for x in self.pos)

def cross(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0] 

def coordRange(points):
    return [max(p.pos[i] for p in points) - min(p.pos[i] for p in points) + 1 for i in range(2)]

def iteratePoints(points):
    best = float('-inf')
    for p1 in points:
        for p2 in points:
            if p1 == p2:
                continue
            
            c = abs(cross(p1.vel, p2.vel))
            if c > best:
                perpVel = [p1, p2]
                best = c

    p1, p2 = perpVel
    for i in range(2):
        if abs(p2.vel[i] - p1.vel[i]) != 0:
            timeSteps = abs(p2.pos[i] - p1.pos[i]) // abs(p2.vel[i] - p1.vel[i])
            break

    timeSteps -= 10
    if timeSteps < 0:
        timeSteps = 0

    for p in points:
        p.applyVel(iterations=timeSteps)

    while True:
        pPoints = copy.deepcopy(points)

        for p in points:
            p.applyVel()

        if coordRange(pPoints) < coordRange(points):
            break

        timeSteps += 1

    return [pPoints, timeSteps]

def printPoints(points):
    points = {str(p): p for p in points}
    mins = [min(p.pos[i] for p in points.values()) for i in range(2)]
    maxs = [max(p.pos[i] for p in points.values()) for i in range(2)]
    
    for y in range(mins[1], maxs[1] + 1):
        for x in range(mins[0], maxs[0] + 1):
            c = '#' if ",".join([str(x), str(y)]) in points else ' '
            print(c, end='')

        print(' ')

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    points = []
    for line in lines:
        points.append(Point(line))

    finalPoints, timeSteps = iteratePoints(points)
    if verbose:
        print("\nPart 1:\nMessage:\n")
        printPoints(finalPoints)
        print(f"\nPart 2:\nMessage appeared after {timeSteps} seconds.")

    return [None, timeSteps]
    

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
