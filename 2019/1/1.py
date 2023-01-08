import time


def rocketFuel(weight):
    newFuel = weight // 3 - 2
    if newFuel <= 0:
        return 0

    newFuel += rocketFuel(newFuel)
    return newFuel
    

def main(verbose):
    with open("input.txt",encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    sum = 0
    for line in lines:
        sum += int(line) // 3 - 2

    part1 = sum

    sum = 0
    for line in lines:
        sum += rocketFuel(int(line))

    if verbose:
        print(f"\nPart 1:\nFuel Required: {part1}\n\nPart 2:\nTotal Fuel Required: {sum}")

    return [part1, sum]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
