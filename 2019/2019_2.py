def part1(data, replace = True):
    """ 2019 Day 2 Part 1

    >>> part1(['1,9,10,3,2,3,11,0,99,30,40,50'], False)
    3500
    >>> part1(['1,1,1,4,99,5,6,0,99'], False)
    30
    """

    lines = [int(x) for x in data[0].split(',')]

    if replace:
        lines[1] = 12
        lines[2] = 2

    return runCode(lines)


def part2(data):
    """ 2019 Day 2 Part 2
    """

    lines = [int(x) for x in data[0].split(',')]

    target = 19690720
    num = runCode(lines[:])
    lines[1] -= 1
    while num != target:
        lines[1] += 1
        lines[2] = 0

        while num < target and lines[2] + 1 < len(lines):
            lines[2] += 1
            num = runCode(lines[:])
    
    return 100 * lines[1] + lines[2]


def runCode(data):
    i = 0
    while data[i] != 99:
        opCode = data[i]
        operands = data[i + 1:i + 3]
        store = data[i + 3]

        if opCode == 1:
            value = 0
            for index in operands:
                value += data[index]

            data[store] = value
        elif opCode == 2:
            value = 1
            for index in operands:
                value *= data[index]

            data[store] = value
        
        i += 4

    return data[0]


def main(verbose = False):
    from pathlib import Path
    import sys, re
    sys.path.append(str(Path(__file__).parent.parent))
    from Modules.timer import Timer
    year, day = re.findall('\d+', str(__file__))[-2:]
    
    with open(Path(__file__).parent.parent / f"Inputs/{year}_{day}.txt", encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    with Timer() as p1_time:
        p1 = part1(data)

    if verbose:
        print(f"\nPart 1:\nValue at index 0: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\n100 * noun + verb: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)