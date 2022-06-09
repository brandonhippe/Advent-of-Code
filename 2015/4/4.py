import time
import hashlib

def main(data = 'bgvyzdsv'):
    i = 0
    p1 = None
    p2 = None
    while p1 is None or p2 is None:
        result = hashlib.md5(f'{data}{i}'.encode()).hexdigest()
        if p1 is None and result[:5] == '00000':
            p1 = i

        if p2 is None and result[:6] == '000000':
            p2 = i

        i += 1

    print(f"\nPart 1:\nFirst number to produce hash starting with at least 5 zeros: {p1}")
    print(f"\nPart 2:\nFirst number to produce hash starting with at least 6 zeros: {p2}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
