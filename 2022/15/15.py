from time import perf_counter
import re


def manhatDist(p1, p2):
    return sum([abs(c1 - c2) for c1, c2 in zip(p1, p2)])


def findIntersection(range1, range2):
    maxX = max(range1[0], range2[0])
    minX = min(range1[1], range2[1])

    if minX >= maxX:
        return (maxX, minX)
    else:
        return 0


def notPossibleP1(sensorData, testLine):
    total = 0
    finished = []

    for sensor, dist in reversed(sensorData):
        intersections = []
        if isinstance(sensor, list):
            if abs(sensor[1] - testLine) > dist:
                continue

            sensorRange = [sensor[0] - (dist - abs(sensor[1] - testLine)), sensor[0] + (dist - abs(sensor[1] - testLine))]
        else:
            sensorRange = [sensor, dist]

        for other in finished:
            intersection = findIntersection(sensorRange, other)

            if intersection != 0:
                intersections.append(intersection)
            
        total += sensorRange[1] - sensorRange[0] + 1
        total -= notPossibleP1(intersections, testLine)

        finished.append(sensorRange)

    return total


def main(filename):
    with open(filename, encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    sensorData = []
    beacons = set()
    for line in lines:
        nums = [int(x) for x in re.findall("-?\d+", line)]
        sensor = nums[:2]
        beacon = nums[2:]

        sensorData.append([sensor, manhatDist(sensor, beacon)])
        beacons.add(tuple(beacon))

    testLine = 10 if '1' in filename else 2000000

    count = notPossibleP1(sensorData, testLine)
    count -= len([b for b in list(beacons) if b[1] == testLine])
    
    print(f"\nPart 1:\n{count}")

    distress = None
    for y in range(testLine * 2 + 1):
        x = 0
        while x <= testLine * 2:
            found = False
            maxEnd = x
            for sensor, d in sensorData:
                if manhatDist(sensor, (x, y)) <= d:
                    found = True
                    rowEnd = sensor[0] + d - abs(y - sensor[1])
                    maxEnd = max(maxEnd, rowEnd)

            if not found:
                distress = (x, y)
                break

            x = maxEnd + 1

        if distress is not None:
            break

    print(f"\nPart 2:\n{distress[0] * 4000000 + distress[1]}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input.txt")
    print(f"\nRan in {perf_counter() - init_time} seconds.")