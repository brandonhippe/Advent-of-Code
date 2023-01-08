import time
import re
from collections import defaultdict

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

def fib(n, memo):    
    if n - 1 in memo:
        tot = memo[n - 1]
    else:
        tot = fib(n - 1, memo)
        memo[n - 1] = tot

    return tot + memo[n - 2]

def calc(regs, nums):
    regs['a'] = fib(regs['d'] + 1, {0: 1, 1: 1})

    return regs['a'] + nums[0] * nums[1]

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        instructions = [line.strip('\n').split(' ') for line in f.readlines()]
    
    regs = defaultdict(lambda: 0)
    while 0 <= regs['PC'] < 9:
        op, *text = instructions[regs['PC']]
        OPS[op](regs, text)
        regs['PC'] += 1

    nums = [int(re.findall('-?\d+', l[1])[0]) for l in instructions[16:18]]
    part1 = calc(regs, nums)

    regs = defaultdict(lambda: 0)
    regs['c'] = 1
    while 0 <= regs['PC'] < 9:
        op, *text = instructions[regs['PC']]
        OPS[op](regs, text)
        regs['PC'] += 1

    nums = [int(re.findall('-?\d+', l[1])[0]) for l in instructions[16:18]]
    part2 = calc(regs, nums)

    if verbose:
        print(f"\nPart 1:\nValue in register a after program executes: {part1}\n\nPart 2:\nValue in register a after program executes: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
