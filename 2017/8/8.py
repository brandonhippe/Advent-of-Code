import time
from collections import defaultdict

def main(filename):
    with open(filename, encoding='UTF-8') as f:
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

    print(f"\nPart 1:\nMaximum value in any register: {max(registers.values())}")
    print(f"\nPart 2:\nMaximum value in any register at any point: {maxVal}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
