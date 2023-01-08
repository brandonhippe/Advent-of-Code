import time

def neighborCells(data, x, y):
    neighbors = []
    
    for yOff in range(-1, 2):
        for xOff in range(-1, 2):
            if not (yOff == 0 or xOff == 0):
                continue
                
            ny = y + yOff
            nx = x + xOff
            if 0 <= ny < len(data) and 0 <= nx < len(data[0]) and [x, y] != [nx, ny]:
                neighbors.append([data[ny][nx], [nx, ny]])

    neighbors.sort(key=neighborSort)
    return neighbors

def neighborSort(e):
    return e[0]

def fillRegion(data, visited, x, y):
    visited[y][x] = True
    size = 1

    neighbors = neighborCells(data, x, y)

    for n in neighbors:
        if not visited[n[1][1]][n[1][0]]:
            size += fillRegion(data, visited, n[1][0], n[1][1])

    return size

def main(verbose):
    with open('input.txt',encoding='UTF-8') as f:
        data = [[int(x) for x in line.strip()] for line in f.readlines()]

    count = 0
    for (i, line) in enumerate(data):
        for (j, p) in enumerate(line):
            neighbors = neighborCells(data, j, i)
            low = True
            for n in neighbors:
                if p >= n[0]:
                    low = False

            if low:
                count += p + 1

    basins = []
    template = [False] * len(data[0])
    visited = []
    for i in range(len(data)):
        visited.append(template[:])
    
    for (i, line) in enumerate(data):
        for (j, p) in enumerate(line):
            if p == 9:
                visited[i][j] = True

    for (i, line) in enumerate(visited):
        for (j, p) in enumerate(line):
            if not p:
                basins.append(fillRegion(data, visited, j, i))

    basins.sort(reverse=True)
    product = 1
    for (i, b) in enumerate(basins[:3]):
        product *= b
    
    if verbose:
        print(f"\nPart 1:\nSum of risk levels of low points: {count}\n\nPart 2:\nProduct of the size of the 3 largest basins: {product}")

    return [count, product]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
