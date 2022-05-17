import time
import re
from collections import defaultdict

def setr(x, y, regs):
    regs[x] = y
    return 0

def sub(x, y, regs):
    regs[x] -= y
    return 0

def mul(x, y, regs):
    regs[x] *= y
    return 1

def jnz(x, y, regs):
    try:
        x = int(x)
    except ValueError:
        x = regs[x]

    if x != 0:
        regs['PC'] += y - 1

    return 0

OPS = {'set': setr, 'sub': sub, 'mul': mul, 'jnz': jnz}

def SieveOfEratosthenes(n):
    primes = defaultdict(lambda: True)
    p = 2
    while (p * p <= n):
        if (primes[p] == True):
            for i in range(p ** 2, n + 1, p):
                primes[i] = False
        p += 1
    primes[0]= False
    primes[1]= False

    return primes

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        instructions = [line.strip('\n') for line in f.readlines()]

    registers = defaultdict(lambda: 0)
    multiplies = 0
    while 0 <= registers['PC'] < len(instructions):
        ins = instructions[registers['PC']]
        op, reg, data = ins.split(' ') + [None] * (3 - len(ins.split(' ')))

        if data is not None:
            try:
                data = int(data)
            except ValueError:
                data = registers[data]

        multiplies += OPS[op](reg, data, registers)
        registers['PC'] += 1

    print(f"\nPart 1:\nNumber of multiplies: {multiplies}")

    registers = defaultdict(lambda: 0)
    registers['a'] = 1
    while registers['PC'] < 8:
        ins = instructions[registers['PC']]
        op, reg, data = ins.split(' ') + [None] * (3 - len(ins.split(' ')))

        if data is not None:
            try:
                data = int(data)
            except ValueError:
                data = registers[data]

        OPS[op](reg, data, registers)
        registers['PC'] += 1

    h = 0
    stepSize = int(re.findall('\d+', instructions[-2])[0])
    b, c = registers['b'], registers['c']
    primes = SieveOfEratosthenes(c)

    for n in range(b, c+1, stepSize):
        if not primes[n]:
            h += 1

    print(f"\nPart 2:\nValue in h: {h}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
