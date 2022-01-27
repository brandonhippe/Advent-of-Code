import time

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    # 0 is horizontal position, 1 is depth
    pos = [0] * 2

    for line in lines:
        split = line.split(' ')
        num = int(split[-1])
        if line[0] == 'f':
            pos[0] += num
        elif line[0] == 'd':
            pos[1] += num
        elif line[0] == 'u':
            pos[1] -= num

    product = 1
    for i in pos:
        product *= i

    print("Part 1:\nProduct: " + str(product))


    pos = [0] * 2
    aim = 0
    for line in lines:
        split = line.split(' ')
        num = int(split[-1])
        if line[0] == 'f':
            pos[0] += num
            pos[1] += num * aim
        elif line[0] == 'd':
            aim += num
        elif line[0] == 'u':
            aim -= num

    product = 1
    for i in pos:
        product *= i

    print("Part 2:\nProduct: " + str(product))

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
