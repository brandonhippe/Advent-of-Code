import time
import re


class Observation:
    def __init__(self, before, op, after) -> None:
        self.prevReg = before
        self.op = op
        self.postReg = after
        self.behavesLike = 0

def addr(reg, op):
    out = reg[:]
    out[op[-1]] = reg[op[1]] + reg[op[2]]
    return out

def addi(reg, op):
    out = reg[:]
    out[op[-1]] = reg[op[1]] + op[2]
    return out

def mulr(reg, op):
    out = reg[:]
    out[op[-1]] = reg[op[1]] * reg[op[2]]
    return out

def muli(reg, op):
    out = reg[:]
    out[op[-1]] = reg[op[1]] * op[2]
    return out

def banr(reg, op):
    out = reg[:]
    out[op[-1]] = reg[op[1]] & reg[op[2]]
    return out

def bani(reg, op):
    out = reg[:]
    out[op[-1]] = reg[op[1]] & op[2]
    return out

def borr(reg, op):
    out = reg[:]
    out[op[-1]] = reg[op[1]] | reg[op[2]]
    return out

def bori(reg, op):
    out = reg[:]
    out[op[-1]] = reg[op[1]] | op[2]
    return out

def setr(reg, op):
    out = reg[:]
    out[op[-1]] = reg[op[1]]
    return out

def seti(reg, op):
    out = reg[:]
    out[op[-1]] = op[1]
    return out

def gtir(reg, op):
    out = reg[:]
    out[op[-1]] = int(op[1] > reg[op[2]])
    return out

def gtri(reg, op):
    out = reg[:]
    out[op[-1]] = int(reg[op[1]] > op[2])
    return out

def gtrr(reg, op):
    out = reg[:]
    out[op[-1]] = int(reg[op[1]] >= reg[op[2]])
    return out

def eqir(reg, op):
    out = reg[:]
    out[op[-1]] = int(op[1] == reg[op[2]])
    return out

def eqri(reg, op):
    out = reg[:]
    out[op[-1]] = int(reg[op[1]] == op[2])
    return out

def eqrr(reg, op):
    out = reg[:]
    out[op[-1]] = int(reg[op[1]] == reg[op[2]])
    return out

def reduceOps(opCodes):
    while max(len(o) for o in opCodes.values()) > 1:
        funPos = {fun: [o for o in opCodes.keys() if fun in opCodes[o]] for fun in OPERATIONS}

        for fun, pos in zip(funPos.keys(), funPos.values()):
            if len(pos) == 1:
                opCodes[pos[0]] = [fun]

        for op, funs in zip(opCodes.keys(), opCodes.values()):
            if len(funs) == 1:
                for op2, funs2 in zip(opCodes.keys(), opCodes.values()):
                    if op == op2:
                        continue

                    if funs[0] in funs2:
                        opCodes[op2].pop(opCodes[op2].index(funs[0]))

OPERATIONS = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    observations = []
    i = 0
    while len(lines[i]) > 0:
        before, op, after, _ = lines[i:i + 4]
        observations.append(Observation([int(n) for n in re.findall('\d+', before)], [int(n) for n in re.findall('\d+', op)], [int(n) for n in re.findall('\d+', after)]))
        i += 4

    program = [[int(n) for n in re.findall('\d+', line)] for line in lines[i + 2:]]

    opCodes = {o: OPERATIONS[:] for o in set(ob.op[0] for ob in observations)}

    for o in observations:
        for fun in OPERATIONS:
            if fun(o.prevReg, o.op) == o.postReg:
                o.behavesLike += 1
            elif fun in opCodes[o.op[0]]:
                opCodes[o.op[0]].pop(opCodes[o.op[0]].index(fun))

    part1 = len([o for o in observations if o.behavesLike >= 3])

    reduceOps(opCodes)
    reg = [0] * 4
    for op in program:
        reg = opCodes[op[0]][0](reg, op)

    if verbose:
        print(f"\nPart 1:\nNumber of observations that behave like 3 or more opcodes: {part1}\n\nPart 2:\nValue in register 0 after program executes: {reg[0]}")

    return [part1, reg[0]]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
