from time import perf_counter

def main(verbose):
    with open("input.txt", encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    sum = 0
    for line in lines:
        priority = list(set(line[:len(line) // 2]) & set(line[len(line) // 2:]))[0]
        if priority.lower() == priority:
            sum += ord(priority) - ord('a') + 1
        else:
            sum += ord(priority) - ord('A') + 27

    part1 = sum

    sum = 0
    for i in range(0, len(lines), 3):
        priority = set(lines[i])
        for j in range(1, 3):
            priority = priority & set(lines[i + j])

        priority = list(priority)[0]

        if priority.lower() == priority:
            sum += ord(priority) - ord('a') + 1
        else:
            sum += ord(priority) - ord('A') + 27

    if verbose:
        print(f"\nPart 1:\nSum of priorities: {part1}\n\nPart 2:\nSum of priorities: {sum}")

    return [part1, sum]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time}")
