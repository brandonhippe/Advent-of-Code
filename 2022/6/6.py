from time import perf_counter

def main(verbose):
    with open("input.txt", encoding="UTF-8") as f:
        line = f.readline().strip()

    for i in range(4, len(line) + 1):
        if len(set(line[i - 4:i])) == 4:
            end = i
            break
    
    part1 = end

    for i in range(14, len(line) + 1):
        if len(set(line[i - 14:i])) == 14:
            end = i
            break

    if verbose:
        print(f"\nPart 1:\nFirst occurrance of non-repeating 4 characters: {part1}\n\nPart 2:\nFirst occurrance of non-repeating 14 characters: {end}")

    return [part1, end]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")