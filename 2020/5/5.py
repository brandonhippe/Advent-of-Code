import time

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        seats = sorted([int(''.join(['1' if c in 'BR' else '0' for c in line.strip('\n')]), 2) for line in f.readlines()])

    for i in range(len(seats)):
        if seats[i] + 1 != seats[i + 1]:
            break

    if verbose:
        print(f"\nPart 1:\nMaximum seat id: {seats[-1]}\n\nPart 2:\nOpen seat: {seats[i] + 1}")

    return [seats[-1], seats[i] + 1]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time}")
