import time
import heapq

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

def handler(state):
    dirs = [[0, 1], [0, -1], [-1, 0], [1, 0]]
    moveOrder = [1, 4, 2, 3]
    loc = [0, 0]

    area = {}
    area[arrToStr(loc)] = 1
    
    while loc != [0, 0] or len(area) == 1:
        #printSpace(area, loc)

        while True:
            state = runCode(state, [moveOrder[0]])[1]
            outputs = state.pop(-1)
            state.append([])

            newLoc = [l + m for (l, m) in zip(loc, dirs[moveOrder[0] - 1])]
            area[arrToStr(newLoc)] = outputs[0]

            if outputs[0] != 0:
                loc = newLoc[:]

                for _ in range(3):
                    moveOrder.append(moveOrder.pop(0))
                
                break

            moveOrder.append(moveOrder.pop(0))

    printSpace(area, loc)
    return area

def arrToStr(arr):
    string = str(arr[0])
    for a in arr[1:]:
        string += ',' + str(a)

    return string

def printSpace(area, loc):
    maxs = [float('-inf')] * 2
    mins = [float('inf')] * 2

    for lStr in area:
        l = [int(x) for x in lStr.split(',')]

        for (i, c) in enumerate(l):
            if c < mins[i]:
                mins[i] = c
            if c > maxs[i]:
                maxs[i] = c

    for y in range(maxs[1], mins[1] - 1, -1):
        for x in range(mins[0], maxs[0] + 1):
            locStr = str(x) + ',' + str(y)
            l = area[locStr] if locStr in area else 0

            c = 'D' if x == loc[0] and y == loc[1] else ('#' if l == 0 else (' ' if l == 1 else '!'))
            print(c,end='')

        print('')

    print('-'*(maxs[0] - mins[0] + 1))

def heuristic(start, end):
    return sum([abs(e - s) for (s, e) in zip(start, end)])

def getNext(curr, area):
    dirs = [[0, 1], [0, -1], [-1, 0], [1, 0]]

    adj = []
    for d in dirs:
        adj.append(arrToStr([l + m for (l, m) in zip(curr, d)]))

    for i in range(len(adj) - 1, -1, -1):
        a = adj[i]
        if a not in area or area[a] == 0:
            adj.pop(i)

    return adj

def aStar(area, start, end):
    openList_heap = [[heuristic(start, end), 0, start]]
    closedList = {}
    heuristics = {}

    heuristics[arrToStr(start)] = heuristic(start, end)

    heapq.heapify(openList_heap)
    while len(openList_heap) != 0:
        qF, qG, q = heapq.heappop(openList_heap)  
        
        if q == end:
            return qG

        nextStates = getNext(q, area)

        for n in nextStates:
            state = [int(x) for x in n.split(',')]
            nG = qG + 1

            if n in heuristics:
                nH = heuristics[n]
            else:
                nH = heuristic(state, end)
                heuristics[n] = nH

            nF = nG + nH

            found = False
            for item in openList_heap:
                if item[2] == state and item[0] <= nF:
                    found = True
                    break

            if found or (n in closedList and closedList[n][0] <= nF):
                continue

            heapq.heappush(openList_heap, [nF, nG, state])

        closedList[arrToStr(q)] = [qF, qG, q]

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [int(l) for l in f.readline().strip().split(',')]

    code = {}
    for (i, x) in enumerate(lines):
        code[i] = x

    area = handler([code, 0, 0, []])

    for (k, v) in zip(area.keys(), area.values()):
        if v == 2:
            end = [int(x) for x in k.split(',')]
            break

    print(f"\nPart 1:\nFewest steps to oxygen system: {aStar(area, [0, 0], end)}")

    maximum = float('-inf')
    for (k, v) in zip(area.keys(), area.values()):
        if v == 0:
            continue
        
        dist = aStar(area, end, [int(x) for x in k.split(',')])

        if dist > maximum:
            maximum = dist

    print(f"\nPart 2:\nIt will take {maximum} minutes to fill with oxygen")

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
