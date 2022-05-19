import time

def dragonCurve(data, disk):
    while len(data) < disk:
        a = data
        b = ''.join('1' if c == '0' else '0' for c in a)
        data = a + '0' + b[::-1]

    return data

def checkSum(data, disk):
    data = dragonCurve(data, disk)
    while True:
        cs = ''
        for i in range(0, min(disk, len(data)), 2):
            cs += '1' if len(set(data[i:i+2])) == 1 else '0'

        data = cs
        if len(data) % 2 == 1:
            break

    return data

def main(data = "01110110101001000", diskP1 = 272, diskP2 = 35651584):
    print(f"\nPart 1:\nChecksum: {checkSum(data, diskP1)}")
    print(f"\nPart 1:\nChecksum: {checkSum(data, diskP2)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
