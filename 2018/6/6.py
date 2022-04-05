import time
import re

def manhatDist(p1, p2):
    return sum([abs(c1 - c2) for c1, c2 in zip(p1, p2)])

def convexHull(points):    
    hull = []
    for point in points:
        x1, y1 = point
        for x2, y2 in points:
            if x1 == x2 and y1 == y2:
                continue

            a = y2 - y1
            b = x1 - x2
            c = x1 * y2 - y1 * x2

            left, right = 0, 0

            for x, y in points:
                if (x == x1 and y == y1) or (x == x2 and y == y2):
                    continue

                if a * x + b * y < c:
                    left += 1
                elif a * x + b * y > c:
                    right += 1

            if left == 0 or right == 0:
                hull.append(point)
                break

    return hull

def main(fileName):
    with open(fileName, encoding='UTF-8') as f:
        points = [[int(x) for x in re.findall('\d+', line.strip('\n'))] for line in f.readlines()]

    hull = convexHull(points)
    regions = {','.join([str(c) for c in point]): [] for point in points if point not in hull}
    
    mins = [min([p[i] for p in hull]) for i in range(len(hull[0]))]
    maxs = [max([p[i] for p in hull]) for i in range(len(hull[0]))]

    for y in range(mins[1], maxs[1] + 1):
        for x in range(mins[0], maxs[0] + 1):
            best = [float('inf'), []]
            for p in points:
                d = manhatDist([x, y], p)
                if d == best[0]:
                    best[1].append(p)
                elif d < best[0]:
                    best = [d, [p]]
            
            if len(best[1]) == 1 and ','.join([str(p) for p in best[1][0]]) in regions:
                regions[','.join([str(p) for p in best[1][0]])].append([x, y])
    
    print(f"\nPart 1:\nSize of the largest finite area: {max(len(s) for s in regions.values())}")

    totDist = 10000 if len(re.findall('\d+', fileName)) == 0 else 32
    closeCount = 0
    for y in range(mins[1], maxs[1] + 1):
        for x in range(mins[0], maxs[0] + 1):
            if sum([manhatDist([x, y], p) for p in points]) < totDist:
                closeCount += 1

    print(f"\nPart 2:\nSize of close region: {closeCount}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
