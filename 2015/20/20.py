import time

def main(data = 33100000):
    houses = [0] * (1 + data // 10)
    for elf in range(1, data // 10 + 1):
        for i in range(elf, data // 10 + 1, elf):
            houses[i] += 10 * elf

    for i, h in enumerate(houses):
        if h >= data:
            break

    print(f"\nPart 1:\nFirst house to receive at least {data} presents: {i}")

    houses = [0] * (1 + data // 10)
    for elf in range(1, data // 10 + 1):
        for i in range(elf, min(data // 10, elf * 50) + 1, elf):
            houses[i] += 11 * elf

    for i, h in enumerate(houses):
        if h >= data:
            break

    print(f"\nPart 2:\nFirst house to receive at least {data} presents: {i}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
