from time import perf_counter
import re
from collections import defaultdict, OrderedDict


def hashAlg(s):
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val %= 256

    return val


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n').split(',') for line in f.readlines()][0]

    part1 = sum(hashAlg(s) for s in lines)

    boxes = defaultdict(lambda: OrderedDict())

    for line in lines:
        label = re.findall('\w+', line)[0]
        box = hashAlg(label)
        
        op = re.findall('[-=]', line)[0]

        if op == '=':
            lens = int(re.findall('\d+', line)[0])
            boxes[box][label] = lens
        elif label in boxes[box]:
            boxes[box].pop(label)

    part2 = 0
    for boxNum, contents in boxes.items():
        boxNum += 1

        for slot, (label, fLen) in enumerate(contents.items()):
            slot += 1
            part2 += boxNum * slot * fLen

    if verbose:
        print(f"\nPart 1:\n{part1}\n\nPart 2:\n{part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
