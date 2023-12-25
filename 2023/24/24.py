from time import perf_counter
from z3 import *
import re


def gaussJordan(augMatrix):
    try:
        for i in range(len(augMatrix[0]) - 1):
            multRow = 1 / augMatrix[i][i]
            for j in range(len(augMatrix[i])):
                augMatrix[i][j] *= multRow

            for j in range(len(augMatrix)):
                if j == i:
                    continue

                subAmt = -augMatrix[j][i]
                augMatrix[j] = list(addVectors(augMatrix[j], (c * subAmt for c in augMatrix[i])))
    except ZeroDivisionError:
        return None
    
    return augMatrix


def isintersect(a1x, a1y, b1x, b1y, a2x, a2y, b2x, b2y, d1x, d1y, d2x, d2y):    
    augMatrix = [[-d1y / d1x, 1, a1y - (d1y * a1x / d1x)], [-d2y / d2x, 1, a2y - (d2y * a2x / d2x)]]
    augMatrix = gaussJordan(augMatrix)
    if augMatrix is None:
        return False

    x = augMatrix[0][-1]
    y = augMatrix[1][-1]

    return min(a1x, b1x) <= x <= max(a1x, b1x) and min(a1y, b1y) <= y <= max(a1y, b1y) and min(a2x, b2x) <= x <= max(a2x, b2x) and min(a2y, b2y) <= y <= max(a2y, b2y)


def intersections(ps, vs, boundMin, boundMax):
    segments = []

    for p, v in zip(ps, vs):
        pChanged = True
        valid = True
        while pChanged and valid:
            pChanged = False
            for i in range(2):
                if p[i] < boundMin:
                    mult = (boundMin - p[i]) / v[i]
                    if mult < 0:
                        valid = False
                        break

                    p = tuple(c + (mult * o) for c, o in zip(p, v))
                    pChanged = True

                if p[i] > boundMax:
                    mult = (boundMax - p[i]) / v[i]
                    if mult < 0:
                        valid = False
                        break

                    p = tuple(c + (mult * o) for c, o in zip(p, v))
                    pChanged = True

        if valid:
            segStart = p
            mult = float('inf')
            for i in range(2):
                if v[i] < 0:
                    mult = min(mult, (boundMin - p[i]) / v[i])
                elif v[i] > 0:
                    mult = min(mult, (boundMax - p[i]) / v[i])

            segEnd = tuple(c + (mult * o) for c, o in zip(p, v))
            segments.append((segStart, segEnd, v))

    intersects = 0
    for i, seg1 in enumerate(segments[:-1]):
        (a1x, a1y), (b1x, b1y), (d1x, d1y) = seg1
        for seg2 in segments[i + 1:]:
            (a2x, a2y), (b2x, b2y), (d2x, d2y) = seg2
            intersects += isintersect(a1x, a1y, b1x, b1y, a2x, a2y, b2x, b2y, d1x, d1y, d2x, d2y)

    return intersects


def addVectors(v1, v2):
    return tuple(c1 + c2 for c1, c2 in zip(v1, v2))


def findCoordinates(positions, velocities, rockVX = None, rockVY = None, rockVZ = None):
    s = Solver()
    pX, pY, pZ = [], [], []
    t = []
    velX = Int('velX')
    velY = Int('velY')
    velZ = Int('velZ')
    posX = Int('posX')
    posY = Int('posY')
    posZ = Int('posZ')

    for i, ((px, py, pz), (vx, vy, vz)) in enumerate(zip(positions, velocities)):
        pX.append(Int(f'pX{i}'))
        pY.append(Int(f'pY{i}'))
        pZ.append(Int(f'pZ{i}'))
        t.append(Int(f't{i}'))
        s.add(pX[i] == px + (t[i] * vx), pY[i] == py + (t[i] * vy), pZ[i] == pz + (t[i] * vz), t[i] != 0)
        s.add(posX + t[i] * velX == pX[i], posY + t[i] * velY == pY[i], posZ + t[i] * velZ == pZ[i])

    if rockVX is not None:
        s.add(velX == rockVX)

    if rockVY is not None:
        s.add(velY == rockVY)

    if rockVZ is not None:
        s.add(velZ == rockVZ)

    # print(s.check())
    if s.check():
        m = s.model()

        return [int(str(m.evaluate(coord))) for coord in [posX, posY, posZ]]
    else:
        return None


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    ps = []
    vs = []
    for line in lines:
        p, v = line.split(' @ ')
        ps.append(tuple(int(n) for n in re.findall('-?\d+', p)))
        vs.append(tuple(int(n) for n in re.findall('-?\d+', v)))

    part1 = intersections([tuple(p[:-1]) for p in ps], [tuple(v[:-1]) for v in vs], 200000000000000, 400000000000000)
    
    posVels = {axis: set(range(-1000, 1001)) for axis in [0, 1, 2]}
    for i in range(len(vs) - 1):
        for j in range(i + 1, len(vs)):
            for ax in range(2):
                if vs[i][ax] != vs[j][ax]:
                    continue
                
                distDiff = abs(ps[i][ax] - ps[j][ax])
                for v in list(posVels[ax]):
                    if v == vs[i][ax] or distDiff % (v - vs[i][ax]) != 0:
                        posVels[ax].remove(v)

    throwPos = findCoordinates(ps, vs, *[list(posVels[i])[0] if len(posVels[i]) == 1 else None for i in sorted(posVels.keys())])

    if throwPos is not None:
        part2 = sum(throwPos)
    else:
        part2 = 0

    if verbose:
        print(f"\nPart 1:\nNumber of 2D Intersections within Area: {part1}\n\nPart 2:\nSum of Coordinates of Rock Throw: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
