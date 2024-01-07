def part1(data):
    """ 2019 Day 5 Part 1
    """

    return runCode([int(l) for l in data[0].split(',')], [1])[-1]


def part2(data):
    """ 2019 Day 5 Part 2
    """

    return runCode([int(l) for l in data[0].split(',')], [5])[-1]


def runCode(data, inputs):
    i = 0
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

    return outputs


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
        print(f"\nPart 1:\nDiagnostic Code: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nDiagnostic Code: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)