import time

def modMultInv(n, m):
    return pow(n, m - 2, m)

def main(verbose):
    data = [1327981, 2822615]
    loopSize = 0
    nums = data[:]
    m = modMultInv(7, 20201227)
    while all(d != 1 for d in nums):
        loopSize += 1
        for i in range(len(data)):
            nums[i] = (nums[i] * m) % 20201227
    
    part1 = pow(data[1] if pow(7, loopSize, 20201227) == data[0] else data[0], loopSize, 20201227)

    if verbose:
        print(f"\nPart 1:\nEncryption key: {part1}")

    return [part1]

if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
