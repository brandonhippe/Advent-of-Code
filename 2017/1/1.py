import time

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = f.readline().strip('\n')

    print(f"\nPart 1:\nCaptcha solution: {sum([int(data[i]) if data[i] == data[(i + 1) % len(data)] else 0 for i in range(len(data))])}")
    print(f"\nPart 2:\nCaptcha solution: {sum([int(data[i]) if data[i] == data[(i + (len(data) // 2)) % len(data)] else 0 for i in range(len(data))])}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
    