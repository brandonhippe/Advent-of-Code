def part1(data):
    """ 2021 Day 7 Part 1

    >>> part1(['16,1,2,0,4,2,7,1,2,14'])
    37
    """

    nums = sorted(int(n) for n in data[0].split(','))

    minFuel = len(nums) * nums[-1]
    for i in range(nums[0], nums[-1] + 1):
        fuel = 0
        for num in nums:
            fuel += abs(i - num)

        if fuel < minFuel:
            minFuel = fuel

    return minFuel


def part2(data):
    """ 2021 Day 7 Part 2

    >>> part2(['16,1,2,0,4,2,7,1,2,14'])
    168
    """

    nums = sorted(int(n) for n in data[0].split(','))

    minFuel = len(nums) * triangle(nums[-1])
    for i in range(nums[0], nums[-1] + 1):
        fuel = 0
        for num in nums:
            fuel += triangle(abs(i - num))

        if fuel < minFuel:
            minFuel = fuel

    return minFuel


def triangle(n):
    return n * (n + 1) // 2


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
        print(f"\nPart 1:\nMinimum fuel: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nMinimum fuel: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)