import time
import re
from collections import defaultdict

from numpy import array

def cpy(regs, text):
    x, y = text
    if len(re.findall('-?\d+', x)) != 0:
        x = int(x)
    else:
        x = regs[x]

    regs[y] = x

def inc(regs, x):
    regs[x[0]] += 1

def dec(regs, x):
    regs[x[0]] -= 1

def jnz(regs, text):
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

def out(regs, x):
    x = x[0]
    if len(re.findall('-?\d+', x)) != 0:
        x = int(x)
    else:
        x = regs[x]

    regs['printed'].append(x)

OPS = {"cpy": cpy, "inc": inc, "dec": dec, "jnz": jnz, "out": out}

def alternatingBits(n):
    n = bin(n)[2:]
    for i in range(1, len(n)):
        if n[i] == n[i - 1]:
            return False

    return True

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        instructions = [line.strip('\n').split(' ') for line in f.readlines()]

    a = 0
    regs = defaultdict(lambda: 0)
    regs['printed'] = []
    regs['a'] = a
    while 0 <= regs['PC'] < 8:
        op, *text = instructions[regs['PC']]
        OPS[op](regs, text)
        regs['PC'] += 1

    while not alternatingBits(regs['d']):
        a += 1
        regs['d'] += 1

    if verbose:
        print(f"\nPart 1:\nValue of a that generates clock signal: {a}")

    return [a]

if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
