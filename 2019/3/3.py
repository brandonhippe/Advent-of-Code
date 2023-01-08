import time

class wire:
    def __init__(self, path):
        self.path = path[:]
        self.path = self.path.split(',')
        self.corners = [[0, 0]]
        for i in path.split(','):
            if i[0] == 'U':
                self.corners.append([item1 + item2 for (item1, item2) in zip(self.corners[-1], [0, int(i[1:])])])
            elif i[0] == 'D':
                self.corners.append([item1 - item2 for (item1, item2) in zip(self.corners[-1], [0, int(i[1:])])])
            elif i[0] == 'L':
                self.corners.append([item1 - item2 for (item1, item2) in zip(self.corners[-1], [int(i[1:]), 0])])
            else:
                self.corners.append([item1 + item2 for (item1, item2) in zip(self.corners[-1], [int(i[1:]), 0])])

class lineSeg:
    def __init__(self, p):
        if p[0][0] == p[1][0]:
            self.horiz = True
            self.vert = False
            self.same = p[0][0]
            self.ends = [p[0][1], p[1][1]]
        elif p[0][1] == p[1][1]:
            self.horiz = False
            self.vert = True
            self.same = p[0][1]
            self.ends = [p[0][0], p[1][0]]

        self.ends.sort()

def manhatDist(p1, p2):
    dist = 0
    for (l1, l2) in zip(p1, p2):
        dist += abs(l1 - l2)

    return dist

def findIntersections(wires):
    intersections = []
    for i in range(len(wires[0].corners) - 1):
        line1 = lineSeg([wires[0].corners[i], wires[0].corners[i + 1]])
        for j in range(len(wires[1].corners) - 1):
            line2 = lineSeg([wires[1].corners[j], wires[1].corners[j + 1]])
            if line1.vert != line2.vert and line2.ends[0] <= line1.same <= line2.ends[1] and line1.ends[0] <= line2.same <= line1.ends[1]:
                intersection = [line1.same if line1.horiz else line2.same, line1.same if line1.vert else line2.same]
                if intersection != [0, 0]:
                    intersections.append(intersection)

    return intersections

def main(verbose):
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    wires = []
    for line in lines:
        wires.append(wire(line))

    intersections = findIntersections(wires)
    manhatDists = []
    for intersection in intersections:
        manhatDists.append(manhatDist(intersection, [0, 0]))

    manhatDists.sort()
    part1 = manhatDists[0]

    delays = [0] * len(intersections)
    for w in wires:
        delay = 0
        point = [0, 0]
        direction = w.path[0][0]
        nextIndex = 1
        encountered = [False] * len(delays)

        while point != w.corners[-1]:
            nextCorner = w.corners[nextIndex]
            if point == nextCorner:
                direction = w.path[nextIndex][0]
                nextIndex += 1

            if point in intersections:
                i = intersections.index(point)
                if not encountered[i]:
                    delays[i] += delay
                    encountered[i] = True

            move = [1 if direction == 'R' else (-1 if direction == 'L' else 0), 1 if direction == 'U' else (-1 if direction == 'D' else 0)]
            point = [item1 + item2 for (item1, item2) in zip(point, move)]
            delay += 1

    delays.sort()

    if verbose:
        print(f"Part 1:\nClosest intersection to central port: {part1}\nPart 2:\nLowest delay is {delays[0]} steps")

    return [part1, delays[0]]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
