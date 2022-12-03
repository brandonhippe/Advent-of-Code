from time import perf_counter

def main(filename):
    with open(filename, encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    sum = 0
    for line in lines:
        priority = list(set(line[:len(line) // 2]) & set(line[len(line) // 2:]))[0]
        if priority.lower() == priority:
            sum += ord(priority) - ord('a') + 1
        else:
            sum += ord(priority) - ord('A') + 27

    print(f"\nPart 1:\n{sum}")

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

    print(f"\nPart 2:\n{sum}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input.txt")
    print(f"\nRan in {perf_counter() - init_time}")
