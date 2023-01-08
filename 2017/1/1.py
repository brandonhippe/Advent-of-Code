import time

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        data = f.readline().strip('\n')

    part1 = sum([int(data[i]) if data[i] == data[(i + 1) % len(data)] else 0 for i in range(len(data))])
    part2 = sum([int(data[i]) if data[i] == data[(i + (len(data) // 2)) % len(data)] else 0 for i in range(len(data))])

    if verbose:
        print(f"\nPart 1:\nCaptcha solution: {part1}\n\nPart 2:\nCaptcha solution: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
    