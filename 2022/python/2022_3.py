def part1(data):
    """ 2022 Day 3 Part 1

    >>> part1(['vJrwpWtwJgWrhcsFMMfFFhFp', 'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL', 'PmmdzqPrVvPwwTWBwg', 'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn', 'ttgJtRGJQctTZtZT', 'CrZsJsPPZsGzwwsLwLmpwMDw'])
    157
    """

    sum = 0
    for line in data:
        priority = list(set(line[:len(line) // 2]) & set(line[len(line) // 2:]))[0]
        if priority.lower() == priority:
            sum += ord(priority) - ord('a') + 1
        else:
            sum += ord(priority) - ord('A') + 27

    return sum


def part2(data):
    """ 2022 Day 3 Part 2

    >>> part2(['vJrwpWtwJgWrhcsFMMfFFhFp', 'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL', 'PmmdzqPrVvPwwTWBwg', 'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn', 'ttgJtRGJQctTZtZT', 'CrZsJsPPZsGzwwsLwLmpwMDw'])
    70
    """

    sum = 0
    for i in range(0, len(data), 3):
        priority = set(data[i])
        for j in range(1, 3):
            priority = priority & set(data[i + j])

        priority = list(priority)[0]

        if priority.lower() == priority:
            sum += ord(priority) - ord('a') + 1
        else:
            sum += ord(priority) - ord('A') + 27

    return sum


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
        print(f"\nPart 1:\nSum of priorities: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nSum of priorities: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)