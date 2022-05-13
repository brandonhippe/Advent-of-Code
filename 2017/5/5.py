import time

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        lines = [int(line.strip('\n')) for line in f.readlines()]

    linesP2 = lines[:]
    ix = 0
    steps = 0
    while 0 <= ix < len(lines):
        jmp = lines[ix]
        lines[ix] += 1
        ix += jmp
        steps += 1

    print(f"\nPart 1:\nSteps before jumping outside list: {steps}")

    lines = linesP2[:]

    ix = 0
    steps = 0
    while 0 <= ix < len(lines):
        jmp = lines[ix]
        lines[ix] += 1 if lines[ix] < 3 else -1
        ix += jmp
        steps += 1

    print(f"\nPart 2:\nSteps before jumping outside list: {steps}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
