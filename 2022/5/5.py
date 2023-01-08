from time import perf_counter
import re

def main(verbose):
    with open("input.txt", encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    crates = []
    
    for n, line in enumerate(lines):
        if len(line) == 0:
            ix = n + 1
            break

        for ix in range(1, len(line), 4):
            if line[ix] != ' ':
                while ix // 4 >= len(crates):
                    crates.append([])

                crates[ix // 4].append(line[ix])

    for i in range(len(crates)):
        crates[i].pop()
        crates[i].reverse()
    
    for line in lines[ix:]:
        qty, start, dest = [int(x) for x in re.findall("\d+", line)]

        while qty != 0:
            qty -= 1
            crates[dest - 1].append(crates[start - 1].pop())

    part1 = ''.join([crate[-1] for crate in crates])

    crates = []
    
    for n, line in enumerate(lines):
        if len(line) == 0:
            ix = n + 1
            break

        for ix in range(1, len(line), 4):
            if line[ix] != ' ':
                while ix // 4 >= len(crates):
                    crates.append([])

                crates[ix // 4].append(line[ix])

    for i in range(len(crates)):
        crates[i].pop()
        crates[i].reverse()
    
    for line in lines[ix:]:
        qty, start, dest = [int(x) for x in re.findall("\d+", line)]
        crates[dest - 1] += crates[start - 1][-qty:]
        crates[start - 1] = crates[start - 1][:-qty]

    part2 = ''.join([crate[-1] for crate in crates])

    if verbose:
        print(f"\nPart 1:\nCrates on top: {part1}\n\nPart 2:\nCrates on top: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")