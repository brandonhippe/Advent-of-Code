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

def dispImage(img):
    for c in img:
        print(chr(c), end='')

def handlerP1(code):
    state = [code, 0, 0, []]
    inputs = [ord(c) for c in "NOT B J\nNOT C T\nOR T J\nAND D J\nNOT A T\nOR T J\nWALK\n"]

    while True:
        result = runCode(state, inputs)

        if result[0]:
            # Code halted
            if result[1][-1] >= 128:
                # Springdroid made it across and found hull damage
                return result[1][-1]
            else:
                dispImage(result[1])
        else:
            # Code needs input
            print("Code requested more input, which could not be provided.")
            return -1

def handlerP2(code):
    state = [code, 0, 0, []]
    inputs = [ord(c) for c in "NOT B J\nNOT C T\nOR T J\nAND D J\nAND H J\nNOT A T\nOR T J\nRUN\n"]

    while True:
        result = runCode(state, inputs)

        if result[0]:
            # Code halted
            if result[1][-1] >= 128:
                # Springdroid made it across and found hull damage
                return result[1][-1]
            else:
                dispImage(result[1])
        else:
            # Code needs input
            print("Code requested more input, which could not be provided.")
            return -1

def main(verbose):
    with open('input.txt', encoding='UTF-8') as f:
        lines = [int(l) for l in f.readline().strip().split(',')]

    code = {}
    for (i, x) in enumerate(lines):
        code[i] = x

    part1 = handlerP1(copy.deepcopy(code))
    part2 = handlerP2(copy.deepcopy(code))

    if verbose:
        print(f"\nPart 1:\nDamage done to hull: {part1}\n\nPart 2:\nDamage done to hull: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
