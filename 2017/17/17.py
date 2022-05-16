import time
from collections import deque

def main(data=316):
    buf = deque([])

    for i in range(50_000_001):
        buf.rotate(-data)
        buf.append(i)

        if i == 2017:
            print(f"\nPart 1:\nNumber after 2017: {buf[0]}")

    print(f"\nPart 2:\nNumber after 50,000,000: {buf[buf.index(0) + 1]}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
