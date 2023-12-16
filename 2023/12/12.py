from time import perf_counter
import re
from functools import cache


@cache
def calcCombs(groups, numbers):
    combs = 0

    groupIx = 0
    while groupIx < len(groups) and len(groups[groupIx]) == 0:
        groupIx += 1

    if groupIx == len(groups):
        return len(numbers) == 0
    elif len(numbers) == 0:
        return all(set(g) == {'?'} for g in groups[groupIx:])

    # If first group is only #'s, check to make sure it matches the first number. If not, return 0
    # If first group does match first number, check if it is only group. If yes, return 1
    # Otherwise, remove fir
    if set(groups[groupIx]) == {'#'}:
        if len(numbers) == 0 or len(groups[groupIx]) != numbers[0]:
            return 0
        
        if len(groups) == 1 + groupIx:
            return len(numbers) == 1
        
        return calcCombs(groups[groupIx + 1:], numbers[1:])

    amt = 0
    for i, c in enumerate(groups[groupIx]):
        if c == '#':        
            # If character in first group is #, increase the amount found
            amt += 1
        else:
            # Check if amt found is consistent with first group. Otherwise, try both . and #
            if amt == 0 or amt == numbers[0]:
                # Conditions to check a .
                newGroups = [groups[groupIx][:i], groups[groupIx][i + 1:]] + list(groups[groupIx + 1:])
                combs += calcCombs(tuple(newGroups), numbers)

            if amt != numbers[0]:
                # Conditions to check a #
                newGroups = [groups[groupIx][:i] + '#' + groups[groupIx][i + 1:]] + list(groups[groupIx + 1:])
                combs += calcCombs(tuple(newGroups), numbers)

            break

    return combs


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    part1 = 0
    part2 = 0
    for line in lines:
        groups, numbers = line.split(' ')
        groups = tuple(re.findall('[#?]+', groups))
        numbers = tuple(int(n) for n in re.findall('\d+', numbers))
        part1 += calcCombs(groups, numbers)

        groups, numbers = line.split(' ')
        groups = '?'.join([groups] * 5)
        numbers = (numbers + ',') * 5
        groups = tuple(re.findall('[#?]+', groups))
        numbers = tuple(int(n) for n in re.findall('\d+', numbers))
        
        part2 += calcCombs(groups, numbers)

    if verbose:
        print(f"\nPart 1:\nSum of possible arrangements: {part1}\n\nPart 2:\nSum of possible arrangements: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
