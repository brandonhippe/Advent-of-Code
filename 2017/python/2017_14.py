def part1(data):
    """ 2017 Day 14 Part 1

    >>> part1(['flqrgnkx'])
    8108
    """

    disk = [[int(x) for x in '0' * (128 - len(bin(int(knotHash([ord(c) for c in data[0] + '-' + str(i)]), 16))[2:])) + bin(int(knotHash([ord(c) for c in data[0] + '-' + str(i)]), 16))[2:]] for i in range(128)]
    return sum([sum(line) for line in disk])


def part2(data):
    """ 2017 Day 14 Part 2

    >>> part2(['flqrgnkx'])
    1242
    """

    disk = [[int(x) for x in '0' * (128 - len(bin(int(knotHash([ord(c) for c in data[0] + '-' + str(i)]), 16))[2:])) + bin(int(knotHash([ord(c) for c in data[0] + '-' + str(i)]), 16))[2:]] for i in range(128)]
    visited = set()
    regions = 0
    for y, line in enumerate(disk):
        for x, s in enumerate(line):
            if s == 1 and (x, y) not in visited:
                regions += 1
                bfs((x, y), disk, visited)

    return regions


def knotHash(bs):
    bs += [17, 31, 73, 47, 23]
    nums = list(range(256))
    
    ss = 0
    currPos = 0
    for _ in range(64):
        for l in bs:
            if l != 0:
                nums = nums[currPos:] + nums[:currPos]
                nums = nums[l - 1::-1] + nums[l:]
                nums = nums[-currPos:] + nums[:-currPos]

            currPos += ss + l
            currPos %= len(nums)
            ss += 1

    denseHash = []
    for i, n in enumerate(nums):
        if i % 16 == 0:
            denseHash.append(0)

        denseHash[-1] = denseHash[-1] ^ n

    return ''.join(['0' * (2 - len(hex(n)[2:])) + hex(n)[2:] for n in denseHash])


def bfs(start, disks, visited):
    openList = [start]

    while len(openList) != 0:
        pos = openList.pop(0)

        for n in [tuple(p + o for p, o in zip(pos, offset)) for offset in [[0, 1], [0, -1], [1, 0], [-1, 0]]]:
            if not n in visited and 0 <= min(n) and 128 > max(n) and disks[n[1]][n[0]] == 1:
                openList.append(n)

        visited.add(pos)


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
        print(f"\nPart 1:\nSquares used: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nNumber of regions: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)