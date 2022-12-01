from time import perf_counter

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    elves = [0]

    for line in lines:
        if len(line) == 0:
            elves.append(0)
        else:
            elves[-1] += int(line)

    elves = sorted(elves, reverse=True)

    print(f"\nPart 1:\nMost calories carried: {elves[0]}")
    print(f"\nPart 2:\nSum of calories carried by 3 highest: {sum(elves[:3])}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input.txt")
    print(f"\nRan in {perf_counter() - init_time} seconds.")
