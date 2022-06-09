import time

def main(data = '3113322113'):
    for iteration in range(50):
        if iteration == 40:
            print(f"\nPart 1:\nLength: {len(data)}")

        newData = ''
        i = 1
        d = data[0]
        count = 1
        while i < len(data):
            if data[i] != d:
                newData += f'{count}{d}'
                d = data[i]
                count = 1
            else:
                count += 1

            i += 1

        newData += f'{count}{d}'
        data = newData

    print(f"\nPart 2:\nLength: {len(data)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
