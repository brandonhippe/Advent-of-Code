from intcode import Intcode


def part1(data, replace = True):
    """ 2019 Day 2 Part 1

    >>> part1(['1,9,10,3,2,3,11,0,99,30,40,50'], False)
    3500
    >>> part1(['1,1,1,4,99,5,6,0,99'], False)
    30
    """

    intcode = Intcode({i: int(x) for i, x in enumerate(data[0].split(','))})

    if replace:
        intcode.set_data(1, 12)
        intcode.set_data(2, 2)

    if not intcode.runCode():
        raise ValueError("Intcode did not halt properly")
    
    return intcode.get_data(0)


def part2(data):
    """ 2019 Day 2 Part 2
    """

    intcode = Intcode({i: int(x) for i, x in enumerate(data[0].split(','))})

    target = 19690720
    num = 0

    noun = intcode.get_data(1)
    verb = intcode.get_data(2)

    while num != target:
        if not intcode.runCode():
            raise ValueError("Intcode did not halt properly")
        
        num = intcode.get_data(0)
        while num < target and verb + 1 < len(intcode.data):
            verb += 1
            intcode.reset()
            intcode.set_data(1, noun)
            intcode.set_data(2, verb)

            if not intcode.runCode():
                raise ValueError("Intcode did not halt properly")
            
            num = intcode.get_data(0)

        if num != target:
            noun += 1
            verb = 0
            intcode.reset()
            intcode.set_data(1, noun)


    return 100 * noun + verb


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
        print(f"\nPart 1:\nValue at index 0: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\n100 * noun + verb: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)