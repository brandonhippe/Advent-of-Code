import time

def main(verbose):
    with open('input.txt',encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    data = lines[0].split(',')

    fishes = [0] * 9
    for (i, num) in enumerate(data):
        data[i] = int(num)
        fishes[data[i]] += 1

    for _ in range(80):
        fishes.append(fishes.pop(0))
        fishes[6] += fishes[8]

    count = 0
    for num in fishes:
        count += num

    part1 = count

    for _ in range(256 - 80):
        fishes.append(fishes.pop(0))
        fishes[6] += fishes[8]

    count = 0
    for num in fishes:
        count += num

    if verbose:
        print(f"\nPart 1:\nNumber of fishes: {part1}\n\nPart 2:\nNumber of fishes: {count}")

    return [part1, count]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
