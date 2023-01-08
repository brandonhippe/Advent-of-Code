import time
import re

def manhatDist(p1, p2):
    d = sum([abs(c2 - c1) for c1, c2 in zip(p1, p2)])
    return d

def iterate(point, nanobots, calculatedPoints):
    neighbors = [(x, y, z) for x in range(point[0] - 1, point[0] + 2) for y in range(point[1] - 1, point[1] + 2) for z in range(point[2] - 1, point[2] + 2)]
    
    if point not in calculatedPoints:
        calculatedPoints[point] = len([n for n in nanobots if manhatDist(n[:-1], point) <= n[-1]])

    maximum = calculatedPoints[point]
    maximumPoint = point

    for n in neighbors:
        if n not in calculatedPoints:
            calculatedPoints[n] = len([b for b in nanobots if manhatDist(b[:-1], n) <= b[-1]])

        if calculatedPoints[n] > maximum or calculatedPoints[n] == maximum and manhatDist(n, (0, 0, 0)) < manhatDist(maximumPoint, (0, 0, 0)):
            maximum = calculatedPoints[n]
            maximumPoint = n

    return maximumPoint

def find(visited, nanobots, cs, dist, offsets, forceCount):
    xs, ys, zs = cs
    ox, oy, oz = offsets
    boxes = []

    for x in range(min(xs), max(xs)+1, dist):
        for y in range(min(ys), max(ys)+1, dist):
            for z in range(min(zs), max(zs)+1, dist):
                count = 0
                for b in nanobots:
                    bdist = b[-1]
                    if dist == 1:
                        calc = manhatDist((x, y, z), b[:-1])
                        if calc <= bdist:
                            count += 1
                    else:
                        calc =  abs((ox+x) - (ox+b[0]))
                        calc += abs((oy+y) - (oy+b[1]))
                        calc += abs((oz+z) - (oz+b[2]))

                        if calc // dist - 3 <= (bdist) // dist:
                            count += 1

                if count >= forceCount:
                    boxes.append((x, y, z, count, abs(x) + abs(y) + abs(z)))

    while len(boxes) > 0:
        best = []
        bestIndex = None

        for i, b in enumerate(boxes):
            if bestIndex is None or b[4] < best[4]:
                best = b
                bestIndex = i

        if dist == 1:
            return best[4], best[3]
        else:
            xs = [best[0], best[0] + dist // 2]
            ys = [best[1], best[1] + dist // 2]
            zs = [best[2], best[2] + dist // 2]
            a, b = find(visited, nanobots, (xs, ys, zs), dist // 2, (ox, oy, oz), forceCount)
            if a is None:
                boxes.pop(bestIndex)
            else:
                return a, b

    return None, None

def bestLoc(nanobots):
    xs, ys, zs = [[n[i] for n in nanobots] + [0] for i in range(3)]

    dist = 1
    while dist < max(xs) - min(xs) or dist < max(ys) - min(ys) or dist < max(zs) - min(zs):
        dist *= 2

    ox, oy, oz = [-min(cs) for cs in [xs, ys, zs]]

    span = 1
    while span < len(nanobots):
        span *= 2

    forceCheck = 1
    visited = {}

    bestPos, bestCount = [None] * 2

    while True:
        if forceCheck not in visited:
            visited[forceCheck] = find(set(), nanobots, (xs, ys, zs), dist, (ox, oy, oz), forceCheck)

        pos, count = visited[forceCheck]

        if pos is None:
            if span > 1:
                span = span // 2
            forceCheck = max(1, forceCheck - span)
        else:
            if bestCount is None or count > bestCount:
                bestPos, bestCount = pos, count
            if span == 1:
                break

            forceCheck += span

    return bestPos

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        nanobots = [tuple([int(x) for x in re.findall('-?\d+', line)]) for line in f.readlines()]

    largestRadius = nanobots[[n[-1] for n in nanobots].index(max([n[-1] for n in nanobots]))]
    inRadius = [n for n in nanobots if manhatDist(largestRadius[:-1], n[:-1]) <= largestRadius[-1]]

    part1 = len(inRadius)
    part2 = bestLoc(nanobots)

    if verbose:
        print(f"\nPart 1:\nNanobots within largest radius: {part1}\n\nPart 2:\nManhattan Distance to location in range of most nanobots: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
