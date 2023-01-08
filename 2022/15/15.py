from time import perf_counter
import re
from shapely import LineString, Polygon, geometry
from shapely.ops import unary_union


def manhatDist(p1, p2):
    return sum([abs(c1 - c2) for c1, c2 in zip(p1, p2)])


def main(verbose):
    filename = "input.txt"
    with open(filename, encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    testLine = 10 if '1' in filename else 2000000
    
    sensorData = []
    beacons = set()
    minX = float('inf')
    maxX = float('-inf')

    for line in lines:
        nums = [int(x) for x in re.findall("-?\d+", line)]
        sensor = tuple(nums[:2])
        beacon = tuple(nums[2:])
        d = manhatDist(sensor, beacon)

        minX = min(minX, sensor[0] - d)
        maxX = max(maxX, sensor[0] + d)

        sensorData.append(Polygon([[sensor[0] + d, sensor[1]], [sensor[0], sensor[1] + d], [sensor[0] - d, sensor[1]], [sensor[0], sensor[1] - d]]))
        beacons.add(beacon)

    part1 = int(LineString([[minX, testLine], [maxX, testLine]]).intersection(unary_union(sensorData)).length) + 1 - len([b for b in beacons if b[1] == testLine])
        
    distressBox = geometry.box(0, 0, testLine * 2, testLine * 2)
    distress = [int(c) + 1 for c in distressBox.difference(unary_union(sensorData)).bounds]

    if verbose:
        print(f"\nPart 1:\n{part1}\n\nPart 2:\n{distress[0] * 4000000 + distress[1]}")

    return [part1, distress[0] * 4000000 + distress[1]]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")