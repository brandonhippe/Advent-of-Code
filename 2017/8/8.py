import time
from collections import defaultdict

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        instructions = f.readlines()

    registers = defaultdict(lambda: 0)
    maxVal = float('-inf')
    for ins in instructions:
        ins = ins.replace('\n', '')
        ins += 'else 0\n'
        ins = ins.replace('inc', '+=')
        ins = ins.replace('dec', '-=')

        exec(ins, {}, registers)
        thisMax = max(registers.values())
        if thisMax > maxVal:
            maxVal = thisMax

    part1 = max(registers.values())

    if verbose:
        print(f"\nPart 1:\nMaximum value in any register: {part1}\n\nPart 2:\nMaximum value in any register at any point: {maxVal}")

    return [part1, maxVal]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
