import time
import numpy as np

def iterate(acres):
    newAcres = np.empty(acres.shape, dtype=acres.dtype)

    for y in range(len(acres)):
        for x in range(len(acres[y])):
            curr = acres[y, x]
            neighbors = np.array([acres[m, n] for n in range(x-1, x+2) for m in range(y-1, y+2) if 0 <= n < len(acres[y]) and 0 <= m < len(acres) and not (n == x and m == y)])
            adjTrees = len([t for t in neighbors if t == '|'])
            adjLumb = len([l for l in neighbors if l == '#'])

            if curr == '.':
                newAcres[y, x] = '|' if adjTrees >= 3 else '.'
            elif curr == '|':
                newAcres[y, x] = '#' if adjLumb >= 3 else '|'
            elif curr == '#':
                newAcres[y, x] = '#' if adjTrees >= 1 and adjLumb >= 1 else '.'

    return newAcres

def counts(acres):
    trees = 0
    lumber = 0
    for y in range(len(acres)):
        for x in range(len(acres[y])):
            if acres[y, x] == '|':
                trees += 1
            elif acres[y, x] == '#':
                lumber += 1

    return [trees, lumber]

def printAcres(acres):
    string = ''
    for y in range(len(acres)):
        for x in range(len(acres[y])):
            string += acres[y, x]

        string += '\n'

    return string

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        acres = np.array([np.array([l for l in line.strip('\n')]) for line in f.readlines()])

    gridStates = {}
    minutes = 0
    while minutes < 1000000000:
        minutes += 1
        acres = iterate(acres)

        if minutes == 10:
            trees, lumber = counts(acres)
            print(f"\nPart 1:\nResource collection value after 10 min: {trees * lumber}")

        gridStr = printAcres(acres)
        if gridStr in gridStates:
            minutes += ((1000000000 - minutes) // (minutes - gridStates[gridStr])) * (minutes - gridStates[gridStr]) 
        else:
            gridStates[gridStr] = minutes

    trees, lumber = counts(acres)
    print(f"\nPart 2:\nResource collection value after 1000000000 min: {trees * lumber}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
