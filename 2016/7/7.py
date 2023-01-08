import time
import re

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

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [re.split(r'\[([^\]]+)\]', line.strip('\n')) for line in f.readlines()]

    tlsSupport = 0
    for line in lines:
        tlsSupport += 1 if any(abba(g) for g in line[::2]) and not any(abba(g) for g in line[1::2]) else 0

    sslSupport = 0
    for line in lines:
        sslSupport += 1 if ababab(line) else 0

    if verbose:
        print(f"\nPart 1:\nIP Addresses that support TLS: {tlsSupport}\n\nPart 2:\nIP Addresses that support SSL: {sslSupport}")

    return [tlsSupport, sslSupport]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
