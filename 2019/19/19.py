import time
import copy

def runCode(state, inputs):
    # Modes: 0: Position, 1: Immediate, 2: Relative
    data, i, relBase, outputs = state

    while True:
        line = data[i] if i in data else 0

        if line == 99:
            # HLT
            break

        opCode = line % 100
        modes = [int(x) for x in str(line // 100)]
        operands = []

        for j in range(i + 1, i + 4):
            operands.append(data[j] if j in data else 0)

        if opCode == 1:
            # ADD
            value = 0
            for op in operands[:-1]:
                mode = modes.pop(-1) if len(modes) != 0 else 0

                if mode == 0:
                    value += data[op] if op in data else 0
                elif mode == 1:
                    value += op
                elif mode == 2:
                    value += data[relBase + op] if relBase + op in data else 0

            mode = modes.pop(-1) if len(modes) != 0 else 0

            if mode == 0:
                data[operands[-1]] = value
            elif mode == 2:
                data[relBase + operands[-1]] = value

            i += 4
        elif opCode == 2:
            # MULT
            value = 1
            for op in operands[:-1]:
                mode = modes.pop(-1) if len(modes) != 0 else 0

                if mode == 0:
                    value *= data[op] if op in data else 0
                elif mode == 1:
                    value *= op
                elif mode == 2:
                    value *= data[relBase + op] if relBase + op in data else 0

            mode = modes.pop(-1) if len(modes) != 0 else 0

            if mode == 0:
                data[operands[-1]] = value
            elif mode == 2:
                data[relBase + operands[-1]] = value

            i += 4
        elif opCode == 3:
            # STR
            mode = modes.pop(-1) if len(modes) != 0 else 0

            if len(inputs) == 0:
                return [False, [data, i, relBase, outputs]]
            else:
                if mode == 0:
                    data[operands[0]] = inputs.pop(0)
                elif mode == 2:
                    data[relBase + operands[0]] = inputs.pop(0)

            i += 2
        elif opCode == 4:
            # OUT
            mode = modes.pop(-1) if len(modes) != 0 else 0

            if mode == 0:
                outputs.append(data[operands[0]] if operands[0] in data else 0)
            elif mode == 1:
                outputs.append(operands[0])
            elif mode == 2:
                outputs.append(data[relBase + operands[0]] if relBase + operands[0] in data else 0)

            i += 2
        elif opCode == 5:
            # JNZ
            mode = modes.pop(-1) if len(modes) != 0 else 0

            if mode == 0:
                value = data[operands[0]] if operands[0] in data else 0
            elif mode == 1:
                value = operands[0]
            elif mode == 2:
                value = data[relBase + operands[0]] if relBase + operands[0] in data else 0

            if value != 0:
                mode = modes.pop(-1) if len(modes) != 0 else 0

                if mode == 0:
                    i = data[operands[1]] if operands[1] in data else 0
                elif mode == 1:
                    i = operands[1]
                elif mode == 2:
                    i = data[relBase + operands[1]] if relBase + operands[1] in data else 0
            else:
                i += 3
        elif opCode == 6:
            # JZ
            mode = modes.pop(-1) if len(modes) != 0 else 0

            if mode == 0:
                value = data[operands[0]] if operands[0] in data else 0
            elif mode == 1:
                value = operands[0]
            elif mode == 2:
                value = data[relBase + operands[0]] if relBase + operands[0] in data else 0

            if value == 0:
                mode = modes.pop(-1) if len(modes) != 0 else 0

                if mode == 0:
                    i = data[operands[1]] if operands[1] in data else 0
                elif mode == 1:
                    i = operands[1]
                elif mode == 2:
                    i = data[relBase + operands[1]] if relBase + operands[1] in data else 0
            else:
                i += 3
        elif opCode == 7:
            # LT
            value = 0
            for (j, op) in enumerate(operands[:-1]):
                mode = modes.pop(-1) if len(modes) != 0 else 0

                if mode == 0:
                    value += (data[op] if op in data else 0) * ((-1) ** j)
                elif mode == 1:
                    value += op * ((-1) ** j)
                elif mode == 2:
                    value += (data[relBase + op] if relBase + op in data else 0) * ((-1) ** j)

            mode = modes.pop(-1) if len(modes) != 0 else 0

            if mode == 0:
                data[operands[-1]] = int(value < 0)
            elif mode == 2:
                data[relBase + operands[-1]] = int(value < 0)

            i += 4
        elif opCode == 8:
            # EQ
            value = 0
            for (j, op) in enumerate(operands[:-1]):
                mode = modes.pop(-1) if len(modes) != 0 else 0

                if mode == 0:
                    value += (data[op] if op in data else 0) * ((-1) ** j)
                elif mode == 1:
                    value += op * ((-1) ** j)
                elif mode == 2:
                    value += (data[relBase + op] if relBase + op in data else 0) * ((-1) ** j)

            mode = modes.pop(-1) if len(modes) != 0 else 0

            if mode == 0:
                data[operands[-1]] = int(value == 0)
            elif mode == 2:
                data[relBase + operands[-1]] = int(value == 0)

            i += 4
        elif opCode == 9:
            # REL BASE
            mode = modes.pop(-1) if len(modes) != 0 else 0

            if mode == 0:
                relBase += data[operands[0]] if operands[0] in data else 0
            elif mode == 1:
                relBase += operands[0]
            elif mode == 2:
                relBase += data[relBase + operands[0]] if relBase + operands[0] else 0

            i += 2

    return [True, outputs]

def handlerP1(code):
    state = [code, 0, 0, []]
    affected = []

    y = 0
    prevStart = 0
    while y < 50:
        x = prevStart
        firstFound = False
        while x < 50:
            if runCode(copy.deepcopy(state), [x, y])[1][0] == 1:
                if not firstFound:
                    firstFound = True
                    prevStart = x
                affected.append([x, y])
            elif firstFound:
                break

            x += 1

        y += 1

    return affected

def handlerP2(code):
    state = [code, 0, 0, []]

    y = 99
    prevStart = 0
    while True:
        x = prevStart
        while True:
            if runCode(copy.deepcopy(state), [x, y])[1][0] == 1:
                prevStart = x

                if runCode(copy.deepcopy(state), [x + 99, y - 99])[1][0] == 1:
                    return [x, y - 99]
                else:
                    break

            x += 1

        y += 1

def printArea(affected):
    for y in range(50):
        for x in range(50):
            c = '.'
            if [x, y] in affected:
                c = '#'
            
            print(c,end='')
        
        print('')

def main(verbose):
    with open('input.txt', encoding='UTF-8') as f:
        lines = [int(l) for l in f.readline().strip().split(',')]

    code = {}
    for (i, x) in enumerate(lines):
        code[i] = x

    affectedArea = handlerP1(code)
    corner = handlerP2(code)

    if verbose:
        print(f"\nPart 1:\nNumber of points affected by Tractor Beam: {len(affectedArea)}\n\nPart 2:\nCorner: {corner}\n10000 * Corner's X + Corner's Y: {10000 * corner[0] + corner[1]}")

    return [len(affectedArea), 10000 * corner[0] + corner[1]]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
