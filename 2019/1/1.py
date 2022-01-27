import time

def rocketFuel(weight):
    newFuel = weight // 3 - 2
    if newFuel <= 0:
        return 0

    newFuel += rocketFuel(newFuel)
    return newFuel

def main():
    with open('input.txt',encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    sum = 0
    for line in lines:
        sum += int(line) // 3 - 2

    print("\nPart 1:\nFuel Required: " + str(sum))

    sum = 0
    for line in lines:
        sum += rocketFuel(int(line))

    print("\nPart 2:\nTotal Fuel Required: " + str(sum))

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
