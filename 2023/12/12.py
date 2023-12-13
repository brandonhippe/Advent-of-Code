from time import perf_counter
import re
from functools import cache


@cache
def countGroups(line):
    return tuple(len(g) for g in re.findall('#+', line))


@cache
def calcCombs(groups, nums):
    if len(groups) < sum(nums):
        return 0
    
    if len(groups) == 0:
        return len(nums) == 0
    
    if len(nums) == 0:
        return '#' not in groups

    if '?' not in groups:
        return countGroups(groups) == nums
    
    combs = 0

    ## Get first ?
    qMarks = [m.start(0) for m in re.finditer('\?', groups)]

    before = groups[:qMarks[0]]
    after = groups[qMarks[0] + 1:]

    # First ? is a .
    beforeNums = countGroups(before)
    if beforeNums == nums[:len(beforeNums)]:
        # Matches, get combs after
        combs += calcCombs(after, nums[len(beforeNums):])

    # First ? is a #
    beforeNums = countGroups(before + '#')
    trimmedNums = nums[:len(beforeNums)]
    # Match all but last, ? might extend group over where we are
    if beforeNums[:-1] == trimmedNums[:-1]:
        if beforeNums[-1] != trimmedNums[-1]:
            # Flip and continue
            combs += calcCombs(before + '#' + after, nums)

        if beforeNums[-1] == trimmedNums[-1] and (len(after) == 0 or after[0] != '#'):
            combs += calcCombs(after[1:], nums[len(beforeNums):])

    return combs


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]


    groups, nums = [], []
    for line in lines:
        g, ns = line.split(' ')
        groups.append(g)
        nums.append(tuple(int(n) for n in ns.split(',')))

    part1 = 0
    part2 = 0
    for g, ns in zip(groups, nums):
        part1 += calcCombs(g, ns)
        part2 += calcCombs('?'.join([g] * 5), ns * 5)

    if verbose:
        print(f"\nPart 1:\n{part1}\n\nPart 2:\n{part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
