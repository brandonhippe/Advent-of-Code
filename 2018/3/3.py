import time
import re

def findIntersection(box1, box2):
    maxX, maxY = [max(box1[i], box2[i]) for i in (0, 1)]
    minX, minY = [min(box1[i], box2[i]) for i in (2, 3)]

    if minX >= maxX and minY >= maxY:
        return [maxX, maxY, minX, minY]
    else:
        return 0

def nonOverlap(data):
    finished = []
    intersections = []

    for box in data:
        for otherBox in finished:
            intersection = findIntersection(box, otherBox)

            if intersection != 0:
                intersections.append(intersection)

        finished.append(box)

    for i, box in enumerate(data):
        for foundIntersection in intersections:
            intersection = findIntersection(box, foundIntersection)
            if intersection != 0:
                break

        if intersection == 0:
            return i + 1

    return -1

def findOverlaps(claims):
    claimed = {}
    overlaps = {}

    for minX, minY, maxX, maxY in claims:
        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                locStr = f"{x},{y}"
                if locStr in claimed:
                    if locStr not in overlaps:
                        overlaps[locStr] = 1
                else:
                    claimed[locStr] = 1

    return len(overlaps.keys())

def main():
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    claims = []
    for line in lines:
        # Creates format [minX, minY, maxX, maxY]
        claims.append([int(x) for x in re.findall('\d+', line)[1:]])
        for i in range(2):
            claims[-1][i + 2] += claims[-1][i] - 1

    print(f"\nPart 1:\nInches of fabric within 2+ claims: {findOverlaps(claims)}")
    print(f"\nPart 2:\nOnly claim with no overlaps: {nonOverlap(claims)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
