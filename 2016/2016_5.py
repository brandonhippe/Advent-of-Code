import hashlib


def part1(data):
    """ 2015 Day 5 Part 1

    >>> part1(['abc'])
    '18f47a30'
    """

    seed = data[0]
    i = 0
    passcode = ''
    while len(passcode) < 8:
        result = hashlib.md5(f'{seed}{i}'.encode()).hexdigest()
        if result[:5] == '00000':
            passcode += result[5]

        i += 1

    return passcode


def part2(data):
    """ 2015 Day 5 Part 2

    >>> part2(['abc'])
    '05ace8e3'
    """

    seed = data[0]
    i = 0
    passcode = [' '] * 8
    while ' ' in passcode:
        result = hashlib.md5(f'{seed}{i}'.encode()).hexdigest()
        if result[:5] == '00000' and result[5] in '01234567' and passcode[int(result[5])] == ' ':
                passcode[int(result[5])] = result[6]

        i += 1

    return ''.join(passcode)


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
        print(f"\nPart 1:\nPasscode: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nPasscode: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)