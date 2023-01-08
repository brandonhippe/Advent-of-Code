import time
import re
from collections import defaultdict
import copy

def cpy(regs, _, text):
    x, y = text
    if len(re.findall('-?\d+', x)) != 0:
        x = int(x)
    else:
        x = regs[x]

    regs[y] = x

def inc(regs, _, x):
    regs[x[0]] += 1

def dec(regs, _, x):
    regs[x[0]] -= 1

def jnz(regs, _, text):
    x, y = text
    
    if len(re.findall('-?\d+', x)) != 0:
        x = int(x)
    else:
        x = regs[x]

    if len(re.findall('-?\d+', y)) != 0:
        y = int(y)
    else:
        y = regs[y]

    if x != 0:
        regs['PC'] += y - 1

TOGGLES = {"cpy": "jnz", "inc": "dec", "dec": "inc", "jnz": "cpy", "tgl": "inc"}

def tgl(regs, instructions, x):
    x = x[0]
    if len(re.findall('-?\d+', x)) != 0:
        x = int(x)
    else:
        x = regs[x]

    ix = regs['PC'] + x
    if 0 <= ix < len(instructions):
        instructions[ix][0] = TOGGLES[instructions[ix][0]]

OPS = {"cpy": cpy, "inc": inc, "dec": dec, "jnz": jnz, "tgl": tgl}

def main(verbose):
    filename = "input.txt"
    with open(filename, encoding='UTF-8') as f:
        instructions = [line.strip('\n').split(' ') for line in f.readlines()]

    instructionsP2 = copy.deepcopy(instructions)
    regs = defaultdict(lambda: 0)
    if '1' not in filename:
        regs['a'] = 7

    while 0 <= regs['PC'] < len(instructions):
        op, *text = instructions[regs['PC']]
        OPS[op](regs, instructions, text)
        regs['PC'] += 1

    part1 = regs['a']

    instructions = instructionsP2
    regs = defaultdict(lambda: 0)
    regs['a'] = 12

    while 0 <= regs['PC'] < len(instructions):
        if regs['PC'] == 4:
            regs['a'] += regs['b'] * regs['d']
            regs['b'] -= 1
            regs['c'] = 2 * regs['b']
            regs['d'] = 0
            regs['PC'] = 16
        else:
            op, *text = instructions[regs['PC']]
            OPS[op](regs, instructions, text)
            regs['PC'] += 1

    part2 = regs['a']

    if verbose:
        print(f"\nPart 1:\nValue sent to safe: {part1}\n\nPart 2:\nValue sent to safe: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
