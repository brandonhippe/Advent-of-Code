import time

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [int(line.strip('\n')) for line in f.readlines()]

    part1 = sum(lines)
    
    history = []
    frequency = 0
    i = 0
    while True:
        if frequency in history:
            break

        history.append(frequency)
        frequency += lines[i]
        i += 1
        i %= len(lines)

    if verbose:
        print(f"\nPart 1:\nResulting frequency: {part1}\n\nPart 2:\nFirst frequency reached twice: {frequency}")

    return [part1, frequency]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
