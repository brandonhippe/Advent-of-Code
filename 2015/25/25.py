import time
import re

def triangle(n):
    return n * (n + 1) // 2

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        pos = [int(x) for x in re.findall('\d+', f.readline())]

    diagIndex = triangle(sum(pos) - 1) - (sum(pos) - 1 - pos[1])
    part1 = (20151125 * pow(252533, diagIndex - 1, 33554393)) % 33554393

    if verbose:
        print(f"\nPart 1:\nCode to give the machine: {part1}")

    return [part1]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
