import itertools

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

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [int(l) for l in f.readline().strip().split(',')]
    
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

    print(f"\nPart 1:\nMaximum Thruster Signal: {largest}")

    orders = list(itertools.permutations(range(5, 10)))

    largest = 0
    for order in orders:
        output = handler(lines[:], order)
        if output > largest:
            largest = output

    print(f"\nPart 2:\nMaximum Thruster Signal: {largest}")

main()
