import math

def minNeighbor(x, y, floorMap):
    min = 10
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i + j) % 2 == 0:
                continue

            nX = x + j
            nY = y + i
            if nX < 0 or nY < 0:
                continue

            try:
                if min > floorMap[nY][nX]:
                    min = floorMap[nY][nX]
            except:
                continue
    
    return min


def main():
    with open('input.txt',encoding='UTF-8') as f:
        lines = f.readlines()

    floorMap = []
    lineLen = len(lines[-1])

    for (i, line) in enumerate(lines):
        lines[i] = int(line)
        temp = lines[i]
        mapLine = [0] * lineLen

        j = -1
        while temp != 0:
            mapLine[j] = (temp % 10) + 1
            temp = int(temp / 10)
            j -= 1

        floorMap.append(mapLine)

    print("Part 1:")
    count = 0
    for (i, line) in enumerate(floorMap):
        for (j, p) in enumerate(line):           
            if p < minNeighbor(j, i, floorMap):
                count += p

    print("Sum of risk levels of low points: " + str(count))

main()