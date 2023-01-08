import time

def main(verbose):
    data = 33100000
    houses = [0] * (1 + data // 10)
    for elf in range(1, data // 10 + 1):
        for i in range(elf, data // 10 + 1, elf):
            houses[i] += 10 * elf

    for i, h in enumerate(houses):
        if h >= data:
            break

    part1 = [data, i]

    houses = [0] * (1 + data // 10)
    for elf in range(1, data // 10 + 1):
        for i in range(elf, min(data // 10, elf * 50) + 1, elf):
            houses[i] += 11 * elf

    for i, h in enumerate(houses):
        if h >= data:
            break

    part2 = [data, i]

    if verbose:
        print(f"\nPart 1:\nFirst house to receive at least {part1[0]} presents: {part1[1]}\n\nPart 2:\nFirst house to receive at least {part2[0]} presents: {part2[1]}")

    return [part1[1], part2[1]]
    

if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
