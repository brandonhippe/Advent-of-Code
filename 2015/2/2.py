import time
import re

def wrappingPaper(box):
    total = box[0] * box[1]
    for i in range(len(box) - 1):
        for j in range(i + 1, len(box)):
            total += 2 * box[i] * box[j]

    return total

def ribbon(box):
    return 2 * (box[0] + box[1]) + volume(box)

def volume(box):
    total = 1
    for side in box:
        total *= side

    return total

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        boxes = [list(sorted(int(x) for x in re.findall('\d+', line))) for line in f.readlines()]

    part1 = sum(wrappingPaper(box) for box in boxes)
    part2 = sum(ribbon(box) for box in boxes)

    if verbose:
        print(f"\nPart 1:\nTotal wrapping paper needed: {part1}\n\nPart 2:\nTotal ribbon needed: {part2}")

    return [part1, part2]
    

if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
