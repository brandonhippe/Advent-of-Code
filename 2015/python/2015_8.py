def part1(data):
    """ 2015 Day 8 Part 1

    "" is 2 characters of code (the two double quotes), but the string contains zero characters.
    "abc" is 5 characters of code, but 3 characters in the string data.
    "aaa\"aaa" is 10 characters of code, but the string itself contains six "a" characters and a single, escaped quote character, for a total of 7 characters in the string data.
    "\x27" is 6 characters of code, but the string itself contains just one - an apostrophe ('), escaped using hexadecimal notation.

    >>> part1([r'""', r'"abc"', r'"aaa\\"aaa"', r'"\\x27"'])
    12

    """

    return sum([len(line) for line in data]) - sum([stringChars(line) for line in data])


def part2(data):
    """ 2015 Day 8 Part 2

    "" encodes to "\"\"", an increase from 2 characters to 6.
    "abc" encodes to "\"abc\"", an increase from 5 characters to 9.
    "aaa\"aaa" encodes to "\"aaa\\\"aaa\"", an increase from 10 characters to 16.
    "\x27" encodes to "\"\\x27\"", an increase from 6 characters to 11.

    >>> part2([r'""', r'"abc"', r'"aaa\\"aaa"', r'"\\x27"'])
    19

    """

    return sum([encodedChars(line) for line in data]) - sum([len(line) for line in data])


def stringChars(line):
    i = 0
    total = 0
    while i < len(line):
        if line[i] == '\\':
            if line[i + 1] == 'x':
                i += 3
            else:
                i += 1
        elif line[i] == '"':
            total -= 1

        total += 1
        i += 1

    return total


def encodedChars(line):
    total = 2
    for l in line:
        total += 1
        if l in '\\"':
            total += 1

    return total


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
        print(f"\nPart 1:\nCharacters of code minus characters in strings: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nCharacters of encoded minus characters in code: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)