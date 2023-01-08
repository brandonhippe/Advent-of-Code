import time
from collections import defaultdict

def sound(x, _, regs1, regs2=None):
    try:
        x = int(x)
    except ValueError:
        x = regs1[x]

    regs1['SOUND'] = x

def setr(x, y, regs1, regs2=None):
    regs1[x] = y

def add(x, y, regs1, regs2=None):
    regs1[x] += y

def mul(x, y, regs1, regs2=None):
    regs1[x] *= y

def mod(x, y, regs1, regs2=None):
    regs1[x] %= y

def recov(x, _, regs1, regs2=None):
    try:
        x = int(x)
    except ValueError:
        x = regs1[x]

    if x != 0:
        regs1['REC'] = regs1['SOUND']

def jgz(x, y, regs1, regs2=None):
    try:
        x = int(x)
    except ValueError:
        x = regs1[x]

    if x > 0:
        regs1['PC'] += y - 1

def send(x, y, regs1, regs2=None):
    try:
        x = int(x)
    except ValueError:
        x = regs1[x]

    regs2['inQueue'].append(x)
    if regs2['state'] == 1:
        regs2['state'] = 0

    regs1['sent'] += 1

def receive(x, y, regs1, regs2=None):
    if len(regs1['inQueue']) == 0:
        regs1['PC'] -= 1
        if regs2['state'] != 0:
            regs1['state'] = 2
            regs2['state'] = 2
        else:
            regs1['state'] = 1
    else:
        regs1[x] = regs1['inQueue'].pop(0)
        regs1['state'] = 0

OPSP1 = {'snd': sound, 'set': setr, 'add': add, 'mul': mul, 'mod': mod, 'rcv': recov, 'jgz': jgz}
OPSP2 = {'snd': send, 'set': setr, 'add': add, 'mul': mul, 'mod': mod, 'rcv': receive, 'jgz': jgz}

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        instructions = [line.strip('\n') for line in f.readlines()]

    registers = defaultdict(lambda: 0)
    while 0 <= registers['PC'] < len(instructions):
        ins = instructions[registers['PC']]
        op, reg, data = ins.split(' ') + [None] * (3 - len(ins.split(' ')))

        if data is not None:
            try:
                data = int(data)
            except ValueError:
                data = registers[data]

        OPSP1[op](reg, data, registers)
        if op == 'rcv' and 'REC' in registers:
            break

        registers['PC'] += 1

    part1 = registers['REC']

    regs1 = defaultdict(lambda: 0)
    regs2 = defaultdict(lambda: 0)
    regs2['p'] = 1
    regs1['inQueue'], regs2['inQueue'] = [], []

    currRegs = regs1
    otherRegs = regs2
    
    while True:
        while currRegs['state'] == 0:
            ins = instructions[currRegs['PC']]
            op, reg, data = ins.split(' ') + [None] * (3 - len(ins.split(' ')))

            if data is not None:
                try:
                    data = int(data)
                except ValueError:
                    data = currRegs[data]

            OPSP2[op](reg, data, currRegs, otherRegs)
            if op == 'rcv' and 'REC' in currRegs:
                break

            currRegs['PC'] += 1

            if not 0 <= currRegs['PC'] < len(instructions):
                currRegs['state'] = 2

        if 0 not in [currRegs['state'], otherRegs['state']]:
            break

        currRegs, otherRegs = otherRegs, currRegs

    if verbose:
        print(f"\nPart 1:\nRecovered sound: {part1}\n\nPart 2:\nNumber of values sent by program 1: {regs2['sent']}")

    return [part1, regs2['sent']]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
