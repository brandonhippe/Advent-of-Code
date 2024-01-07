import itertools


def part1(data):
    """ 2019 Day 7 Part 1

    >>> part1(['3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'])
    43210
    >>> part1(['3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'])
    54321
    >>> part1(['3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'])
    65210
    """

    lines = [int(l) for l in data[0].split(',')]
    orders = list(itertools.permutations(range(5)))
    
    largest = 0
    for order in orders:
        output = 0
        for o in order:
            inputs = [o, output]
            output = runCode(0, lines[:], inputs)[-1]
            output = output[0]

        if output > largest:
            largest = output

    return largest


def part2(data):
    """ 2019 Day 7 Part 2

    >>> part2(['3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'])
    139629729
    >>> part2(['3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'])
    18216
    """

    lines = [int(l) for l in data[0].split(',')]
    orders = list(itertools.permutations(range(5, 10)))

    largest = 0
    for order in orders:
        output = handler(lines[:], order)
        if output > largest:
            largest = output

    return largest


def runCode(i, data, inputs):
    outputs = []
    while data[i] != 99:
        opCode = data[i] % 100
        modes = [int(x) for x in str(data[i] // 100)]
        operands = data[i + 1:i + 4]

        if opCode == 1:
            # ADD
            value = 0
            for op in operands[:-1]:
                mode = modes.pop(-1) if len(modes) > 0 else 0

                if mode == 0:
                    value += data[op]
                else:
                    value += op

            data[operands[-1]] = value
            
            i += 4
        elif opCode == 2:
            # MULT
            value = 1
            for op in operands[:-1]:
                mode = modes.pop(-1) if len(modes) > 0 else 0

                if mode == 0:
                    value *= data[op]
                else:
                    value *= op

            data[operands[-1]] = value

            i += 4
        elif opCode == 3:
            # STR
            if len(inputs) == 0:
                return [[False, i, data, []], outputs]
            else:
                data[operands[0]] = inputs.pop(0)
                i += 2
        elif opCode == 4:
            # OUT
            outputs.append(data[operands[0]])
            i += 2
        elif opCode == 5:
            # JNZ
            mode = modes.pop(-1) if len(modes) > 0 else 0

            if mode == 0:
                value = data[operands[0]]
            else:
                value = operands[0]

            if value != 0:
                mode = modes.pop(-1) if len(modes) > 0 else 0

                if mode == 0:
                    i = data[operands[1]]
                else:
                    i = operands[1]
            else:
                i += 3
        elif opCode == 6:
            # JZ
            mode = modes.pop(-1) if len(modes) > 0 else 0

            if mode == 0:
                value = data[operands[0]]
            else:
                value = operands[0]

            if value == 0:
                mode = modes.pop(-1) if len(modes) > 0 else 0

                if mode == 0:
                    i = data[operands[1]]
                else:
                    i = operands[1]
            else:
                i += 3
        elif opCode == 7:
            # LT
            value = 0
            for (j, op) in enumerate(operands[:-1]):
                mode = modes.pop(-1) if len(modes) > 0 else 0

                if mode == 0:
                    value += data[op] * ((-1) ** j)
                else:
                    value += op * ((-1) ** j)

            data[operands[-1]] = int(value < 0)
            
            i += 4
        elif opCode == 8:
            # EQ
            value = 0
            for (j, op) in enumerate(operands[:-1]):
                mode = modes.pop(-1) if len(modes) > 0 else 0

                if mode == 0:
                    value += data[op] * ((-1) ** j)
                else:
                    value += op * ((-1) ** j)

            data[operands[-1]] = int(value == 0)
            
            i += 4

    return [[True, i, data, []], outputs]


def handler(data, ampNums):
    amplifierStates = []
    for num in ampNums:
        amplifierStates.append([False, 0, data[:], [num]])

    pOutput = 0
    while (True):
        for (i, state) in enumerate(amplifierStates):
            _, j, code, inputs = state
            inputs.append(pOutput)

            amplifierStates[i], pOutput = runCode(j, code, inputs) 
            pOutput = pOutput[0]           

        if sum(list(s[0] for s in amplifierStates)) == 5:
            break

    return pOutput


def main(verbose = False):
    from pathlib import Path
    import sys, re
    sys.path.append(str(Path(__file__).parent.parent))
    from Modules.timer import Timer
    year, day = re.findall('\d+', str(__file__))[-2:]
    
    with open(Path(__file__).parent.parent / f"Inputs/{year}_{day}.txt", encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    with Timer() as p1_time:
        p1 = part1(data)

    if verbose:
        print(f"\nPart 1:\nMaximum Thruster Signal: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nMaximum Thruster Signal: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)