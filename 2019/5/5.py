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

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [int(l) for l in f.readline().strip().split(',')]

    print(f"\nPart 1:\nDiagnostic Code: {runCode(lines[:], [1])[-1]}")
    print(f"\nPart 2:\nDiagnostic Code: {runCode(lines[:], [5])[-1]}")

main()
