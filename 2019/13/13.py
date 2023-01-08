import time

class tile:
    def __init__(self, info):
        self.x, self.y, self.id = info
        self.string = str(self.x) + ',' + str(self.y)

        if self.x == -1 and self.y == 0:
            self.score = self.id
            self.id = 5

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

def handler(code, playGame=False):
    state = [code, 0, 0, []]
    inputs = []

    tiles = {}

    while True:
        result = runCode(state, inputs)

        if result[0]:
            # Code halted
            for i in range(0, len(result[1]), 3):
                newT = tile(result[1][i:i+3])
                tiles[newT.string] = newT

            return tiles
        else:
            # Code requested more input
            state = result[-1]
            output = state.pop(-1)
            state.append([])

            ballX = -1
            paddleX = -1
            for i in range(0, len(output), 3):
                newT = tile(output[i:i+3])

                if newT.id == 3:
                    paddleX = newT.x

                if newT.id == 4:
                    ballX = newT.x

                tiles[newT.string] = newT

            if playGame:
                printGame(tiles)

            if ballX == paddleX:
                inputs = [0]
            else:
                inputs = [abs(ballX - paddleX) // (ballX - paddleX)]

def printGame(tiles):
    maxs = [float('-inf')] * 2

    for tName in tiles:
        t = tiles[tName]

        if t.x > maxs[0]:
            maxs[0] = t.x

        if t.y > maxs[1]:
            maxs[1] = t.y

    for y in range(maxs[1] + 1):
        for x in range(maxs[0] + 1):
            t = tiles[str(x) + ',' + str(y)]

            c = ' ' if t.id == 0 else ('|' if t.id == 1 and y != 0 else ('-' if t.id == 1 and y == 0 else ('#' if t.id == 2 else ('_' if t.id == 3 else '.'))))
            print(c,end='')

        print('')

def main(verbose):
    with open('input.txt', encoding='UTF-8') as f:
        lines = [int(l) for l in f.readline().strip().split(',')]

    code = {}
    for (i, x) in enumerate(lines):
        code[i] = x

    tiles = handler(code)

    count = 0
    for tName in tiles:
        t = tiles[tName]
        if t.id == 2:
            count += 1

    #printGame(tiles)

    code = {}
    for (i, x) in enumerate(lines):
        code[i] = x

    code[0] = 2

    tiles = handler(code)

    for tName in tiles:
        t = tiles[tName]
        
        if t.id == 5:
            break

    if verbose:
        print(f"\nPart 1:\nNumber of block tiles: {count}\n\nPart 2:\nScore after playing game: {t.score}")

    return [count, t.score]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
