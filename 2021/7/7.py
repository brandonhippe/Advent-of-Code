import time

def triangle(n):
    return n * (n + 1) // 2

def main():
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

    print("Part 1:\nMinimum fuel: " + str(minFuel))

    minFuel = len(data) * triangle(data[-1])
    for i in range(data[0], data[-1]):
        fuel = 0
        for num in data:
            fuel += triangle(abs(i - num))

        if fuel < minFuel:
            minFuel = fuel

    print("Part 2:\nMinimum fuel: " + str(minFuel))

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
