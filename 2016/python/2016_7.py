import re


def part1(data):
    """ 2016 Day 7 Part 1

    abba[mnop]qrst supports TLS (abba outside square brackets).
    abcd[bddb]xyyx does not support TLS (bddb is within square brackets, even though xyyx is outside square brackets).
    aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior characters must be different).
    ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even though it's within a larger string).

    >>> part1(['abba[mnop]qrst', 'abcd[bddb]xyyx', 'aaaa[qwer]tyui', 'ioxxoj[asdfgh]zxcvbn'])
    2
    """

    lines = [re.split(r'\[([^\]]+)\]', line.strip('\n')) for line in data]

    tlsSupport = 0
    for line in lines:
        tlsSupport += 1 if any(abba(g) for g in line[::2]) and not any(abba(g) for g in line[1::2]) else 0

    return tlsSupport


def part2(data):
    """ 2016 Day 7 Part 2

    aba[bab]xyz supports SSL (aba outside square brackets with corresponding bab within square brackets).
    xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).
    aaa[kek]eke supports SSL (eke in supernet with corresponding kek in hypernet; the aaa sequence is not related, because the interior character must be different).
    zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has a corresponding bzb, even though zaz and zbz overlap).

    >>> part2(['aba[bab]xyz', 'xyx[xyx]xyx', 'aaa[kek]eke', 'zazbz[bzb]cdb'])
    3
    """

    lines = [re.split(r'\[([^\]]+)\]', line.strip('\n')) for line in data]

    sslSupport = 0
    for line in lines:
        sslSupport += 1 if ababab(line) else 0

    return sslSupport


def abba(group):
    for i in range(len(group) - 3):
        if group[i] == group[i + 3] and group[i + 1] == group[i + 2] and group[i] != group[i + 1]:
            return True

    return False


def ababab(line):
    superNet = '  '.join(g for g in line[::2])
    hyperNet = '  '.join(g for g in line[1::2])

    for i in range(len(superNet) - 2):
        if superNet[i] == ' ':
            continue

        if superNet[i] == superNet[i + 2] != superNet[i + 1] and superNet[i + 1] + superNet[i] + superNet[i + 1] in hyperNet:
            return True

    return False


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
        print(f"\nPart 1:\nIP Addresses that support TLS: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nIP Addresses that support SSL: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)