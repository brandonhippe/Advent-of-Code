import time

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    points = []
    folds = 0
    for line in lines:
        if len(line) == 0:
            continue

        if line[0] == 'f':
            info = line.split("fold along ")
            info = info[1:]
            info = info[0].split('=')
            info[-1] = int(info[-1])

            if info[0] == 'x':
                newPoints = []
                for point in points:
                    newPoint = [info[1] - abs(point[0] - info[1]), point[1]]
                    if not newPoint in newPoints:
                        newPoints.append(newPoint)

                points = newPoints[:]
            else:
                newPoints = []
                for point in points:
                    newPoint = [point[0], info[1] - abs(point[1] - info[1])]
                    if not newPoint in newPoints:
                        newPoints.append(newPoint)

                points = newPoints[:]

            if folds == 0:
                print("Part 1:\nNumber of dots visible after first fold: " + str(len(points)))
                folds += 1              
        else:
            digits = [int(num) for num in line.split(',')]
            if not digits in points:
                points.append(digits)

    print("\nPart 2:")
    mins = [float('inf')] * 2
    maxs = [float('-inf')] * 2
    for point in points:
        for (i, j) in enumerate(point):
            if j > maxs[i]:
                maxs[i] = j
            
            if j < mins[i]:
                mins[i] = j

    for y in range(mins[1], maxs[1] + 1):
        for x in range(mins[0], maxs[0] + 1):
            c = ' '
            if [x, y] in points:
                c = '#'

            print(c, end='')

        print(' ')

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
