import copy


def part1(data):
    """ 2019 Day 19 Part 1
    """

    return len(handlerP1({i: int(x) for i, x in enumerate(data[0].split(','))}))


def part2(data):
    """ 2019 Day 19 Part 2
    """

    corner = handlerP2({i: int(x) for i, x in enumerate(data[0].split(','))})
    return 10000 * corner[0] + corner[1]


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
        print(f"\nPart 1:\nNumber of points affected by Tractor Beam: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\n10000 * Corner's X + Corner's Y: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)