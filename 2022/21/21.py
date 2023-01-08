from time import perf_counter
import re


def yellResult(monkeys, currM):
    if currM == 'humn':
        return None

    if len(monkeys[currM]) == 1:
        return int(monkeys[currM][0])

    m1, op, m2 = monkeys[currM]
    m1Res = yellResult(monkeys, m1)
    m2Res = yellResult(monkeys, m2)

    if m1Res is not None and m2Res is not None:
        if op == '+':
            return m1Res + m2Res

        if op == '-':
            return m1Res - m2Res

        if op == '*':
            return m1Res * m2Res
            
        if op == '/':
            return m1Res // m2Res
    else:
        return None


def traceBack(monkeys, currM, desired = None):
    if currM == 'humn':
        monkeys['humn'] = desired
        return desired

    yell = [yellResult(monkeys, m) for m in monkeys[currM][::2]]

    op = monkeys[currM][1]
    
    ix = (yell.index(None) + 1) % 2

    if desired is None:
        desired = yell[ix]

    if op == '+':
        newDesired = desired - yell[ix]
    elif op == '-':
        if ix == 0:
            newDesired = yell[ix] - desired
        else:
            newDesired = desired + yell[ix]
    elif op == '*':
        newDesired = desired // yell[ix]
    elif op == '/':
        if ix == 0:
            newDesired = yell[ix] // desired
        else:
            newDesired = desired * yell[ix]
    elif op == '=':
        newDesired = desired

    return traceBack(monkeys, monkeys[currM][ix - 1], newDesired)


def main(verbose):
    with open("input.txt", encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    monkeys = {}
    while len(monkeys) != len(lines) and 'root' not in monkeys:
        for line in lines:
            monkey = line[:4]
            if monkey in monkeys:
                continue
            
            if len(re.findall('-?\d+', line)) != 0:
                monkeys[monkey] = [int(x) for x in re.findall('-?\d+', line)][0]
            else:
                _, m1, op, m2 = line[4:].split(' ')
                if m1 in monkeys and m2 in monkeys:
                    if op == '+':
                        monkeys[monkey] = monkeys[m1] + monkeys[m2]
                    elif op == '-':
                        monkeys[monkey] = monkeys[m1] - monkeys[m2]
                    elif op == '*':
                        monkeys[monkey] = monkeys[m1] * monkeys[m2]
                    elif op == '/':
                        monkeys[monkey] = monkeys[m1] // monkeys[m2]
    
    part1 = monkeys['root']

    monkeys = {line.split(': ')[0]: line.split(': ')[1].split(' ') for line in lines}
    monkeys['root'][1] = '='

    part2 = traceBack(monkeys, 'root')

    if verbose:
        print(f"\nPart 1:\n{part1}\n\nPart 2:\n{part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")