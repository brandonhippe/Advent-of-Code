import time
import copy

def runCode(state, inputs):
    # Modes: 0: Position, 1: Immediate, 2: Relative
    data, i, relBase, outputs = state

    line = data[i] if i in data else 0

    if line == 99:
        # HLT
        return [True, outputs]
        
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

    return [False, [data, i, relBase, outputs]]

def handlerP1(code):
    state = [code, 0, 0, []]

    NICs = []
    inputs = {}
    for i in range(50):
        NICs.append(copy.deepcopy(state))
        inputs[i] = [i]

    while True:
        for (i, n) in enumerate(NICs):
            NICs[i] = runCode(n, inputs[i])[-1]
            
            if len(NICs[i][-1]) == 3:
                if NICs[i][-1][0] == 255:
                    return NICs[i][-1][-1]

                if -1 in inputs[NICs[i][-1][0]]:
                    inputs[NICs[i][-1][0]].pop(inputs[NICs[i][-1][0]].index(-1))

                inputs[NICs[i][-1][0]] += NICs[i][-1][1:]
                NICs[i][-1] = []

        for inp, arr in zip(inputs.keys(), inputs.values()):
            if len(arr) == 0:
                inputs[inp].append(-1)

def handlerP2(code):
    state = [code, 0, 0, []]

    Nat = []
    NICs = []
    inputs = {}
    for i in range(50):
        NICs.append(copy.deepcopy(state))
        inputs[i] = [i]
    
    lastY = float('inf')
    sleeping = [False] * 50
    lastInput = [0] * 50
    period = [0] * 50
    step = 0
    while True:
        if False not in sleeping:
            if Nat[-1] == lastY:
                return lastY
            
            lastY = Nat[-1]
            inputs[0] = Nat[:]
            sleeping[0] = False

        for (i, n) in enumerate(NICs):
            if sleeping[i]:
                continue
            
            emptyInput = inputs[i][-1] == -1
            pLen = len(inputs[i])
            NICs[i] = runCode(n, inputs[i])[-1]
            if emptyInput and pLen != 0 and len(inputs[i]) == 0:
                if step - lastInput[i] == period[i]:
                    sleeping[i] = True
                
                period[i] = step - lastInput[i]
                lastInput[i] = step
            
            if len(NICs[i][-1]) == 3:
                if NICs[i][-1][0] == 255:
                    Nat = NICs[i][-1][1:]
                else:
                    if -1 in inputs[NICs[i][-1][0]]:
                        inputs[NICs[i][-1][0]].pop(inputs[NICs[i][-1][0]].index(-1))
                        sleeping[NICs[i][-1][0]] = False

                    inputs[NICs[i][-1][0]] += NICs[i][-1][1:]
                    
                NICs[i][-1] = []

        for inp, arr in zip(inputs.keys(), inputs.values()):
            if len(arr) == 0:
                inputs[inp].append(-1)

        step += 1


def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [int(l) for l in f.readline().strip().split(',')]

    code = {}
    for (i, x) in enumerate(lines):
        code[i] = x

    print(f"\nPart 1:\nY value of first packet sent to address 255: {handlerP1(copy.deepcopy(code))}")
    print(f"\nPart 2:\nFirst Y value delivered by the NAT to the computer at address 0 twice in a row: {handlerP2(copy.deepcopy(code))}")
    
init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
