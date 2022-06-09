import time
from collections import defaultdict
import re

def hlf(regs, r):
    regs[r[0]] /= 2

def tpl(regs, r):
    regs[r[0]] *= 3

def inc(regs, r):
    regs[r[0]] += 1

def jmp(regs, o):
    regs['PC'] += int(o[0]) - 1

def jie(regs, vals):
    if regs[vals[0]] % 2 == 0:
        regs['PC'] += int(vals[1]) - 1

def jio(regs, vals):
    if regs[vals[0]] == 1:
        regs['PC'] += int(vals[1]) - 1

OPS = {'hlf': hlf, 'tpl': tpl, 'inc': inc, 'jmp': jmp, 'jie': jie, 'jio': jio}

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        instructions = [re.split(',? ', line.strip('\n')) for line in f.readlines()]

    regs = defaultdict(lambda: 0)
    while 0 <= regs['PC'] < len(instructions):
        ins = instructions[regs['PC']]
        OPS[ins[0]](regs, ins[1:])

        regs['PC'] += 1

    print(f"\nPart 1:\nValue in register b after program runs: {regs['b']}")

    regs = defaultdict(lambda: 0)
    regs['a'] = 1
    while 0 <= regs['PC'] < len(instructions):
        ins = instructions[regs['PC']]
        OPS[ins[0]](regs, ins[1:])

        regs['PC'] += 1

    print(f"\nPart 2:\nValue in register b after program runs: {regs['b']}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
