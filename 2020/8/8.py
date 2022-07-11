import time
from collections import defaultdict

def runCode(instructions):
    regs = defaultdict(lambda: 0)
    ran = set()
    while regs['PC'] not in ran and 0 <= regs['PC'] < len(instructions):
        ran.add(regs['PC'])
        op, val = instructions[regs['PC']]
        if op == 'acc':
            regs['acc'] += int(val)
        elif op == 'jmp':
            regs['PC'] += int(val) - 1

        regs['PC'] += 1

    return [regs['acc'], regs['PC'] not in ran]

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        instructions = [line.strip('\n').split(' ') for line in f.readlines()]    

    print(f"\nPart 1:\nValue in accumulator before running any line of code twice: {runCode(instructions)[0]}")

    for i, (op, val), in enumerate(instructions):
        if op == 'acc':
            continue

        acc, result = runCode(instructions[:i] + [['jmp' if op == 'nop' else 'nop', val]] + instructions[i + 1:])
        if result:
            break

    print(f"\nPart 2:\nValue in accumulator after running fixed program: {acc}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
