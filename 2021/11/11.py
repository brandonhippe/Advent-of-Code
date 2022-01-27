import time

def neighborOctopi(data, x, y):
    neighbors = []
    
    for yOff in range(-1, 2):
        for xOff in range(-1, 2):
            if yOff == 0 and xOff == 0:
                continue
                
            ny = y + yOff
            nx = x + xOff
            if 0 <= ny < len(data) and 0 <= nx < len(data[0]) and [x, y] != [nx, ny]:
                neighbors.append([nx, ny])

    return neighbors

def updateOcto(data, x, y):
    if data[y][x] == 10:
        return 0

    count = 0
    data[y][x] += 1

    if data[y][x] == 10:
        count += 1
        nOctos = neighborOctopi(data, x, y)
        for n in nOctos:
            count += updateOcto(data, n[0], n[1])
    
    return count

def main():
    with open('input.txt', encoding='UTF-8') as f:
        data = [[int(x) for x in line.strip()] for line in f.readlines()]

    print("Part 1:")
    count = 0
    for day in range(100):
        for i in range(len(data)):
            for j in range(len(data[i])):
                count += updateOcto(data, j, i)
        
        for i in range(len(data)):
            for j in range(len(data[i])):
                data[i][j] = data[i][j] % 10

    print("Number of Octopi flashes: " + str(count))

    print("Part 2:")
    count = 0
    day = 0
    while count != len(data) * len(data[0]):
        day += 1
        count = 0

        for i in range(len(data)):
            for j in range(len(data[i])):
                data[i][j] = data[i][j] % 10

        for i in range(len(data)):
            for j in range(len(data[i])):
                count += updateOcto(data, j, i)        

    print("First Synchronized Flash: " + str(day + 100))

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
