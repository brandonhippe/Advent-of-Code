def part1(data):
    """ 2020 Day 25 Part 1

    >>> part1(['5764801', '17807724'])
    14897079
    """

    nums = [int(line) for line in data]
    loopSize = 0
    n = nums[:]
    m = modMultInv(7, 20201227)
    while all(d != 1 for d in n):
        loopSize += 1
        for i in range(len(data)):
            n[i] = (n[i] * m) % 20201227
    
    return pow(nums[1] if pow(7, loopSize, 20201227) == nums[0] else nums[0], loopSize, 20201227)


def part2(data):
    """ 2020 Day 25 Part 2
    """

    return "Christmas has been saved!"


def modMultInv(n, m):
    return pow(n, m - 2, m)


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
        print(f"\nPart 1:\n{p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\n{p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)