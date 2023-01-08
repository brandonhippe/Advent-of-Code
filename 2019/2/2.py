import time

def runCode(data):
    i = 0
    while data[i] != 99:
        opCode = data[i]
        operands = data[i + 1:i + 3]
        store = data[i + 3]

        if opCode == 1:
            value = 0
            for index in operands:
                value += data[index]

            data[store] = value
        elif opCode == 2:
            value = 1
            for index in operands:
                value *= data[index]

            data[store] = value
        
        i += 4

    return data[0]


def main(verbose):
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]
    
    data = [int(x) for x in lines[0].split(',')]

    tempData = data[:]
    tempData[1] = 12
    tempData[2] = 2

    part1 = runCode(tempData)

    target = 19690720
    tempData = data[:]
    num = runCode(tempData)
    data[1] -= 1
    while num != target:
        data[1] += 1
        data[2] = 0

        while num < target and data[2] + 1 < len(data):
            data[2] += 1
            tempData = data[:]
            num = runCode(tempData)
    
    part2 = 100 * data[1] + data[2]

    if verbose:
        print(f"\nPart 1:\nValue at index 0: {part1}\n\nPart 2:\n100 * noun + verb: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
