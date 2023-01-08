import time

def triangle(n):
    return n * (n + 1) // 2

def main(verbose):
    with open('input.txt',encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    data = lines[0].split(',')
    for (i, num) in enumerate(data):
        data[i] = int(num)

    data.sort()

    minFuel = len(data) * data[-1]
    for i in range(data[0], data[-1]):
        fuel = 0
        for num in data:
            fuel += abs(i - num)

        if fuel < minFuel:
            minFuel = fuel

    part1 = minFuel

    minFuel = len(data) * triangle(data[-1])
    for i in range(data[0], data[-1]):
        fuel = 0
        for num in data:
            fuel += triangle(abs(i - num))

        if fuel < minFuel:
            minFuel = fuel

    if __name__ == "__main__":
        print(f"\nPart 1:\nMinimum fuel: {part1}\n\nPart 2:\nMinimum fuel: {minFuel}")

    return [part1, minFuel]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
