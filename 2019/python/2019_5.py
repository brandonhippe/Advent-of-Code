from intcode import Intcode


def part1(data):
    """ 2019 Day 5 Part 1
    """

    intcode = Intcode({i: int(x) for i, x in enumerate(data[0].split(','))})
    intcode.addInput(1)
    if not intcode.runCode():
        raise ValueError("Intcode did not halt properly")
    
    return intcode.getOutput()[-1]


def part2(data):
    """ 2019 Day 5 Part 2
    """

    intcode = Intcode({i: int(x) for i, x in enumerate(data[0].split(','))})
    intcode.addInput(5)
    if not intcode.runCode():
        raise ValueError("Intcode did not halt properly")
    
    return intcode.getOutput()[-1]


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
        print(f"\nPart 1:\nDiagnostic Code: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nDiagnostic Code: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)