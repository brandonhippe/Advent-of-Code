import time

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
    inputs = []

    while True:
        result = runCode(state, inputs)

        if result[0]:
            # Code halted
            string = ''
            for c in result[1]:
                string += chr(c)

            return string
        else:
            # Code needs input
            print("Code requested more input, which could not be provided.")
            return -1

def handlerP2(code, mainLine, funcs):
    code[0] = 2
    state = [code, 0, 0, []]
    inputs = []

    for c in mainLine:
        inputs.append(ord(c))

    inputs.append(ord('\n'))

    for v in funcs.values():
        for c in v:
            inputs.append(ord(c))

        inputs.append(ord('\n'))

    inputs.append(ord('n'))
    inputs.append(ord('\n'))

    while True:
        result = runCode(state, inputs)

        if result[0]:
            # Code halted
            return result[1][-1]
        else:
            # Code needs input
            print("Code requested more input, which could not be provided.")
            return -1

def orderCorners(scaffolding, robot, end, corners):
    orderedCorners = []
    offsets = [[[0, 1], [0, -1]], [[1, 0], [-1, 0]]]

    for offsetIndex in range(len(offsets)):
        pOffset = None
        for o in offsets[offsetIndex]:
            n = [r + c for (r, c) in zip(robot, o)]
            if not (n[0] < 0 or n[0] >= len(scaffolding[0]) or n[1] < 0 or n[1] >= len(scaffolding) or scaffolding[n[1]][n[0]] == '.'):
                pOffset = o
                break

        if pOffset:
            break

    while robot != end:
        n = [r + o for (r, o) in zip(robot, pOffset)]

        if n[0] < 0 or n[0] >= len(scaffolding[0]) or n[1] < 0 or n[1] >= len(scaffolding) or scaffolding[n[1]][n[0]] == '.':
            offsetIndex += 1
            offsetIndex = offsetIndex % 2

            for o in offsets[offsetIndex]:
                n = [r + c for (r, c) in zip(robot, o)]
                if not (n[0] < 0 or n[0] >= len(scaffolding[0]) or n[1] < 0 or n[1] >= len(scaffolding) or scaffolding[n[1]][n[0]] == '.'):
                    pOffset = o
                    break

        robot = n[:]

        if n in corners:
            orderedCorners.append(n)

    return orderedCorners

def functions(mainLine, funcs, func):
    start = 0
    while start < len(mainLine) and ((ord('A') <= ord(mainLine[start]) <= ord('C')) or (mainLine[start] == ',')):
        start += 1

    if func == 'D':
        return [start == len(mainLine) and len(mainLine) <= 20, mainLine]

    for i in range(3, 21):
        finalMain = mainLine[:]
        group = finalMain[start:start + i]
        
        if 'A' in group or 'B' in group or 'C' in group:
            break

        if not (finalMain[start + i] == ',' and (finalMain[start + i + 1] == 'L' or finalMain[start + i + 1] == 'R') or ord('A') <= ord(finalMain[start + i + 1]) <= ord('C')):
            continue

        funcs[func] = group[:]

        finalMain = finalMain.replace(group, func)

        result = functions(finalMain, funcs, chr(ord(func) + 1))

        if result[0]:
            return result

    return [False, mainLine]

def generateFunctions(path, orientation):
    mainLine = ','
    while len(path) > 1:
        pos = path.pop(0)

        if pos[0] == path[0][0]:
            goalOrientation = 2 if path[0][1] > pos[1] else 0
        else:
            goalOrientation = 1 if path[0][0] > pos[0] else 3

        mainLine += 'R,' if (orientation + 1) % 4 == goalOrientation else 'L,'

        orientation = goalOrientation

        while len(path) > 1 and (pos[0] == path[0][0] == path[1][0] or pos[1] == path[0][1] == path[1][1]):
            path.pop(0)

        mainLine += str(sum([abs(l - c) for (l, c) in zip(pos, path[0])])) + ','

    funcs = {'A': '', 'B': '', 'C': ''}
    result = functions(mainLine[1:-1], funcs, 'A')

    if result[0]:
        return [result[1], funcs]
                
    return 0

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [int(l) for l in f.readline().strip().split(',')]

    code = {}
    for (i, x) in enumerate(lines):
        code[i] = x

    scaffolding = [line for line in handlerP1(code).split('\n') if len(line) > 0]

    corners = []
    count = 0
    for (y, line) in enumerate(scaffolding):
        for (x, c) in enumerate(line):
            if c == '#':
                vert = 0
                horiz = 0

                if y + 1 < len(scaffolding) and scaffolding[y + 1][x] != '.':
                    vert += 1

                if y - 1 >= 0 and scaffolding[y - 1][x] != '.':
                    vert += 1

                if x + 1 < len(line) and scaffolding[y][x + 1] != '.':
                    horiz += 1

                if x - 1 >= 0 and scaffolding[y][x - 1] != '.':
                    horiz += 1

                if vert + horiz == 1:
                    end = [x, y]

                if vert >= 1 and horiz >= 1:
                    corners.append([x, y])

                if vert + horiz >= 3:
                    scaffolding[y] = scaffolding[y][:x] + 'O' + scaffolding[y][x + 1:]
                    count += (x * y)

            if c == "^" or c == "v" or c == "<" or c == ">":
                orientation = 0 if c == '^' else (1 if c == '>' else (2 if c == 'v' else 3))
                robot = [x, y]

    for line in scaffolding:
        print(line)

    print(f"\nPart 1:\nSum of alignment parameters: {count}")

    corners = orderCorners(scaffolding, robot, end, corners)

    repeats = []

    for (i, c) in enumerate(corners):
        if c in corners[i + 1:]:
            repeats.append([i, i + 1 + corners[i + 1:].index(c)])

    for _ in range(2 ** len(repeats)):
        flip = [x == '1' for x in bin(_)[:1:-1] + '0' * (len(repeats) - len(bin(_)[:1:-1]))]

        path = corners[:]
        for (f, indexes) in zip(flip, repeats):
            if f:
                reversedPart = path[indexes[0] + 1:indexes[1]]
                reversedPart.reverse()
                for (i, c) in enumerate(reversedPart):
                    path[indexes[0] + i + 1] = c

        path.reverse()
        path.append(robot)
        path.reverse()
        path.append(end)

        instructions = generateFunctions(path, orientation)
        if instructions != 0:
            break

    code = {}
    for (i, x) in enumerate(lines):
        code[i] = x

    print(f"\nPart 2:\nDust collected: {handlerP2(code, instructions[0], instructions[1])}")

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
