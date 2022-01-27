import time

def main():
    with open('input.txt',encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    data = lines[0].split(',')

    fishes = [0] * 9
    for (i, num) in enumerate(data):
        data[i] = int(num)
        fishes[data[i]] += 1

    for _ in range(80):
        fishes.append(fishes.pop(0))
        fishes[6] += fishes[8]

    print("Part 1:")
    count = 0
    for num in fishes:
        count += num
    print("Number of fishes: " + str(count))

    for _ in range(256 - 80):
        fishes.append(fishes.pop(0))
        fishes[6] += fishes[8]

    print("Part 2:")
    count = 0
    for num in fishes:
        count += num
    print("Number of fishes: " + str(count))

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
