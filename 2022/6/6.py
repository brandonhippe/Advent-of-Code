from time import perf_counter

def main(filename):
    with open(filename, encoding="UTF-8") as f:
        line = f.readline().strip()

    for i in range(4, len(line) + 1):
        if len(set(line[i - 4:i])) == 4:
            end = i
            break

    print(f"\nPart 1:\nFirst occurrance of non-repeating 4 characters: {end}")

    for i in range(14, len(line) + 1):
        if len(set(line[i - 14:i])) == 14:
            end = i
            break

    print(f"\nPart 2:\nFirst occurrance of non-repeating 14 characters: {end}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input.txt")
    print(f"\nRan in {perf_counter() - init_time} seconds.")