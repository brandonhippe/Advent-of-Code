import time

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
    out[op[-1]] = 1 if op[1] > reg[op[2]] else 0
    return out

def gtri(reg, op):
    out = reg[:]
    out[op[-1]] = 1 if reg[op[1]] > op[2] else 0
    return out

def gtrr(reg, op):
    out = reg[:]
    out[op[-1]] = 1 if reg[op[1]] > reg[op[2]] else 0
    return out

def eqir(reg, op):
    out = reg[:]
    out[op[-1]] = 1 if op[1] == reg[op[2]] else 0
    return out

def eqri(reg, op):
    out = reg[:]
    out[op[-1]] = 1 if reg[op[1]] == op[2] else 0
    return out

def eqrr(reg, op):
    out = reg[:]
    out[op[-1]] = 1 if reg[op[1]] == reg[op[2]] else 0
    return out

OPERATIONS = {  
    'addr': addr, 
    'addi': addi,
    'mulr': mulr, 
    'muli': muli,
    'banr': banr,
    'bani': bani,
    'borr': borr,
    'bori': bori,
    'setr': setr,
    'seti': seti,
    'gtir': gtir,
    'gtri': gtri,
    'gtrr': gtrr,
    'eqir': eqir,
    'eqri': eqri,
    'eqrr': eqrr
}

def factor(num):
    factors = []

    largestFound = 1
    i = 1
    while i < num // largestFound:
        if num % i == 0:
            factors.append(i)
            factors.append(num // i)
            largestFound = i

        i += 1

    return factors

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        program = [line.strip('\n').split(' ') for line in f.readlines()]

    bound = int(program[0][1])
    program = program[1:]

    for line in program:
        for i, s in enumerate(line):
            try:
                line[i] = int(s)
            except ValueError:
                pass

    registers = [0] * 6
    while registers[bound] != 1:
        registers = OPERATIONS[program[registers[bound]][0]](registers, program[registers[bound]])
        registers[bound] += 1

    part1 = sum(factor(registers[5]))

    registers = [0] * 6
    registers[0] = 1
    while registers[bound] != 1:
        registers = OPERATIONS[program[registers[bound]][0]](registers, program[registers[bound]])
        registers[bound] += 1

    part2 = sum(factor(registers[5]))

    if verbose:
        print(f"\nPart 1:\nValue left in register 0 after process halts: {part1}\n\nPart 2:\nValue left in register 0 after process halts: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
