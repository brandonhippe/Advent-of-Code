from intcode import Intcode


def part1(data):
    """ 2019 Day 21 Part 1
    """

    return handlerP1(Intcode({i: int(x) for i, x in enumerate(data[0].split(','))}))


def part2(data):
    """ 2019 Day 21 Part 2
    """

    return handlerP2(Intcode({i: int(x) for i, x in enumerate(data[0].split(','))}))


def dispImage(img):
    for c in img:
        print(chr(c), end='')


def handlerP1(intcode: Intcode):
    inputs = [ord(c) for c in "NOT B J\nNOT C T\nOR T J\nAND D J\nNOT A T\nOR T J\nWALK\n"]
    while True:
        intcode.addInput(inputs)
        if intcode.runCode():
            output = intcode.getOutput()
            if output[-1] >= 128:
                return output[-1]
            else:
                dispImage(output)
                return
        else:
            raise Exception("Code requested more input, which could not be provided.")
        

def handlerP2(intcode: Intcode):
    inputs = [ord(c) for c in "NOT B J\nNOT C T\nOR T J\nAND D J\nAND H J\nNOT A T\nOR T J\nRUN\n"]
    while True:
        intcode.addInput(inputs)
        if intcode.runCode():
            output = intcode.getOutput()
            if output[-1] >= 128:
                return output[-1]
            else:
                dispImage(output)
                return
        else:
            raise Exception("Code requested more input, which could not be provided.")


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
        print(f"\nPart 1:\nDamage done to hull: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nDamage done to hull: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)