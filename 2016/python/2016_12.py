import re
from collections import defaultdict
from functools import cache


def part1(data):
    """ 2016 Day 12 Part 1

    >>> part1(['cpy 41 a', 'inc a', 'inc a', 'dec a', 'jnz a 2', 'dec a'])
    42
    """

    instructions = [line.split(' ') for line in data]

    regs = defaultdict(lambda: 0)
    while 0 <= regs['PC'] < min(9, len(instructions)):
        op, *text = instructions[regs['PC']]
        OPS[op](regs, text)
        regs['PC'] += 1

    return calc(regs, [int(re.findall('-?\d+', l[1])[0]) for l in instructions[16:18]]) if regs['PC'] < len(instructions) else regs['a']


def part2(data):
    """ 2016 Day 12 Part 2
    """

    instructions = [line.split(' ') for line in data]

    regs = defaultdict(lambda: 0)
    regs['c'] = 1
    while 0 <= regs['PC'] < min(9, len(instructions)):
        op, *text = instructions[regs['PC']]
        OPS[op](regs, text)
        regs['PC'] += 1

    return calc(regs, [int(re.findall('-?\d+', l[1])[0]) for l in instructions[16:18]])


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
    y = int(y)
    if len(re.findall('-?\d+', x)) != 0:
        x = int(x)
    else:
        x = regs[x]

    if x != 0:
        regs['PC'] += y - 1


OPS = {"cpy": cpy, "inc": inc, "dec": dec, "jnz": jnz}


@cache
def fib(n):    
    if n <= 1:
        return 1

    return fib(n - 1) + fib(n - 2)


def calc(regs, nums):
    regs['a'] = fib(regs['d'] + 1)

    return regs['a'] + nums[0] * nums[1]


def main(verbose = False):
    from pathlib import Path
    import sys, re
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from Modules.timer import Timer
    year, day = re.findall('\d+', str(__file__))[-2:]
    
    with open(Path(__file__).parent.parent.parent / f"Inputs/{year}_{day}.txt", encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    with Timer() as p1_time:
        p1 = part1(data)

    if verbose:
        print(f"\nPart 1:\nValue in register a after program executes: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nValue in register a after program executes: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)