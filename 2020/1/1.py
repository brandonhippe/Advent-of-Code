import time

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        data = [int(line) for line in f.readlines()]

    data = sorted(data)

    found = False
    for i in range(len(data) - 1):
        for j in range(i + 1, len(data)):
            if data[i] + data[j] == 2020:
                found = True
                break

        if found:
            break

    part1 = data[i] * data[j]


    found = False
    for i in range(len(data) - 2):
        for j in range(i + 1, len(data) - 1):
            for k in range(j + 1, len(data)):
                if data[i] + data[j] + data[k] == 2020:
                    found = True
                    break

            if found:
                break

        if found:
            break

    if verbose:
        print(f"\nPart 1:\nProduct of numbers that sum to 2020: {part1}\n\nPart 2:\nProduct of numbers that sum to 2020: {data[i] * data[j] * data[k]}")

    return [part1, data[i] * data[j] * data[k]]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
    