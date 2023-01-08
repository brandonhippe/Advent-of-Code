import time

def main(verbose):
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    for (i, line) in enumerate(lines):
        lines[i] = int(line)

    increased = 0
    for i in range(1, len(lines)):
        if lines[i] > lines[i - 1]:
            increased += 1

    part1 = increased
    
    increased = 0
    for i in range(3, len(lines)):
        sums = [0] * 2
        frame1 = lines[i - 3:i]
        frame2 = lines[i - 2:i + 1]
        for j in range(3):
            sums[0] += frame1[j]
            sums[1] += frame2[j]

        if sums[1] > sums[0]:
            increased += 1

    if verbose:
        print(f"\nPart1:\nNumber of increases: {part1}\n\nPart 2:\nNumber of increases {increased}")

    return [part1, increased]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
