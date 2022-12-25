from time import perf_counter

NUM = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
STRING = {-2: '=', -1: '-', 0: '0', 1: '1', 2: '2'}


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    num = 0
    for line in lines:
        mult = 1
        for c in line[::-1]:
            num += NUM[c] * mult
            mult *= 5

    part1 = []
    while num != 0:
        part1.append(num % 5)
        num //= 5

    for i, c in enumerate(part1):
        if c not in STRING:
            if i == len(part1) - 1:
                part1.append(0)

            part1[i + 1] += 1
            c -= 5

        part1[i] = STRING[c]

    part1 = ''.join(reversed(part1))

    if verbose:
        print(f"\nPart 1:\nSNAFU Number: {part1}")

    return [part1]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")