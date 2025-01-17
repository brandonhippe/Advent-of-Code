def part1(data):
    """ 2021 Day 6 Part 1

    >>> part1(['3,4,3,1,2'])
    5934
    """

    nums = data[0].split(',')

    fishes = [0] * 9
    for (i, num) in enumerate(nums):
        nums[i] = int(num)
        fishes[nums[i]] += 1

    for _ in range(80):
        fishes.append(fishes.pop(0))
        fishes[6] += fishes[8]

    return sum(fishes)


def part2(data):
    """ 2021 Day 6 Part 2

    >>> part2(['3,4,3,1,2'])
    26984457539
    """

    nums = data[0].split(',')

    fishes = [0] * 9
    for (i, num) in enumerate(nums):
        nums[i] = int(num)
        fishes[nums[i]] += 1

    for _ in range(256):
        fishes.append(fishes.pop(0))
        fishes[6] += fishes[8]

    return sum(fishes)


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
        print(f"\nPart 1:\nNumber of fishes: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nNumber of fishes: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)