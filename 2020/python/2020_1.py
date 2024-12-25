def part1(data):
    """ 2020 Day 1 Part 1

    >>> part1(['1721', '979', '366', '299', '675', '1456'])
    514579
    """

    nums = sorted([int(line) for line in data])

    found = False
    for i in range(len(nums) - 1):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == 2020:
                found = True
                break

        if found:
            break

    return nums[i] * nums[j]


def part2(data):
    """ 2020 Day 1 Part 2

    >>> part2(['1721', '979', '366', '299', '675', '1456'])
    241861950
    """

    nums = sorted([int(line) for line in data])

    found = False
    for i in range(len(nums) - 2):
        for j in range(i + 1, len(nums) - 1):
            for k in range(j + 1, len(nums)):
                if nums[i] + nums[j] + nums[k] == 2020:
                    found = True
                    break

            if found:
                break

        if found:
            break

    return nums[i] * nums[j] * nums[k]


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
        print(f"\nPart 1:\nProduct of numbers that sum to 2020: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nProduct of numbers that sum to 2020: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)