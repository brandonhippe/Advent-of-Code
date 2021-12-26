import re


def volume(box):
    vol = 1
    for i in range(0, len(box), 2):
        vol *= box[i + 1] - box[i] + 1

    return vol

def findIntersection(box1, box2):
    maxX, maxY, maxZ = [max(box1[i], box2[i]) for i in (0, 2, 4)]
    minX, minY, minZ = [min(box1[i], box2[i]) for i in (1, 3, 5)]

    if minX >= maxX and minY >= maxY and minZ >= maxZ:
        return [maxX, minX, maxY, minY, maxZ, minZ]
    else:
        return 0

def countLit(data):
    total = 0
    finished = []

    for line in reversed(data):
        op = line[0]
        box = line[1]

        if op == "on":
            intersections = []
            for other in finished:
                otherOp = other[0]
                otherBox = other[1]

                intersection = findIntersection(box, otherBox)

                if intersection != 0:
                    intersections.append(["on", intersection])
                
            total += volume(box)
            total -= countLit(intersections)

        finished.append(line)

    return total

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]
    
    prismsP1 = []
    prisms = []

    for line in lines:
        line = line.split(" ")
        groups = line[1].split(",")
        bounds = []
        part1 = True
        for group in groups:
            group = group.split("=")[1]
            for x in group.split(".."):
                bounds.append(int(x))
                if abs(int(x)) > 50:
                    part1 = False

        if part1:
            prismsP1.append([line[0], bounds])

        prisms.append([line[0], bounds])

    print("\nPart 1:\nNumber on in Central Core: " + str(countLit(prismsP1)))
    print("\nPart 2:\nNumber on in Reactor: " + str(countLit(prisms)))

main()
