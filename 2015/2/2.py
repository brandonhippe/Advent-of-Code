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

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        boxes = [list(sorted(int(x) for x in re.findall('\d+', line))) for line in f.readlines()]

    print(f"\nPart 1:\nTotal wrapping paper needed: {sum(wrappingPaper(box) for box in boxes)}")
    print(f"\nPart 2:\nTotal ribbon needed: {sum(ribbon(box) for box in boxes)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
