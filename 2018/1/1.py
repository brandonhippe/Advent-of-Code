import time

def main():
    with open("input.txt", encoding='UTF-8') as f:
        lines = [int(line.strip('\n')) for line in f.readlines()]
    
    print(f"\nPart 1:\nResulting frequency: {sum(lines)}")

    history = []
    frequency = 0
    i = 0
    while True:
        if frequency in history:
            break

        history.append(frequency)
        frequency += lines[i]
        i += 1
        i %= len(lines)

    print(f"\nPart 2:\nFirst frequency reached twice: {frequency}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"Ran in {time.perf_counter() - init_time} seconds.")
