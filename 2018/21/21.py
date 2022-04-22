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

def main(filename):
    with open(filename, encoding='UTF-8') as f:
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
    while registers[bound] < len(program):
        if registers[bound] == 28:
            print(f"\nPart 1:\nLowest R0 value for minimum halting time: {registers[2]}")
            break

        registers = OPERATIONS[program[registers[bound]][0]](registers, program[registers[bound]])
        registers[bound] += 1

    r0_cycle = set()
    while registers[bound] < len(program):
        if registers[bound] == 28:
            if registers[2] in r0_cycle:
                print(f"\nPart 2:\nLowest R0 value for maximum halting time: {prev}")
                break
            else:
                r0_cycle.add(registers[2])
                prev = registers[2]

        if registers[bound] == 17:
            registers[3] = registers[5] // program[19][2]
            registers[bound] = 26

        registers = OPERATIONS[program[registers[bound]][0]](registers, program[registers[bound]])
        registers[bound] += 1

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
