import time, sys
sys.path.insert(0,"C:/Users/Brandon Hippe/Documents/Coding Projects/Advent-of-Code/Modules")
from progressbar import printProgressBar

def FFTP1(data):
    basePattern = [0, 1, 0, -1]
    newData = []
    while len(newData) < len(data):
        val = 0
        for (i, d) in enumerate(data):
            repeat = len(newData) + 1
            index = i + 1
            index = index // repeat
            mult = basePattern[((i + 1) // repeat) % 4]
            val += mult * d
        
        newData.append(abs(val) % 10)

    return newData

def FFTP2(data):
    newData = [0]
    for d in data[::-1]:
        newData.append((d + newData[-1]) % 10)

    return newData[-1:0:-1]

def main(verbose):
    with open('input.txt', encoding='UTF-8') as f:
        data = f.readline().strip()

    dataP1 = [int(x) for x in data]
    for i in range(100):
        dataP1 = FFTP1(dataP1)
        if verbose:
            printProgressBar(i + 1, 100)
    
    part1 = sum([val * 10 ** (7 - i) for (i, val) in enumerate(dataP1[:8])])

    dataP2 = data * 10000
    offset = int(dataP2[:7])
    dataP2 = [int(x) for x in dataP2[offset:]]

    for i in range(100):
        dataP2 = FFTP2(dataP2)
        if verbose:
            printProgressBar(i + 1, 100)

    part2 = sum([val * 10 ** (7 - i) for (i, val) in enumerate(dataP2[:8])])

    if verbose:    
        print(f"\nPart 1:\nFirst 8 digits after 100 phases: {part1}\n\nPart 2:\nMessage: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
