def get_adjacent_cells(data, x_coord, y_coord):
    result = []
    for x,y in [(x_coord+i,y_coord+j) for i in (-1,0,1) for j in (-1,0,1) if i == 0 or j == 0]:
        if 0 <= y < len(data) and 0 <= x < len(data[0]) and ((x,y) != (x_coord, y_coord)):
            result.append(data[y][x])
    return result

def main():
    with open('input.txt',encoding='UTF-8') as f:
        data = [[int(x) for x in line.strip()] for line in f.readlines()]

    print("Part 1:")
    count = 0
    for (i, line) in enumerate(data):
        for (j, p) in enumerate(line):
            neighbors = get_adjacent_cells(data, j, i)
            low = True
            for n in neighbors:
                if p >= n:
                    low = False

            if low:
                count += p + 1

    print("Sum of risk levels of low points: " + str(count))

main()