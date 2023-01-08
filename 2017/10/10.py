import time

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        text = f.readline().strip('\n')
        bs = [ord(x) for x in text] + [17, 31, 73, 47, 23]
        lengths = [int(x) for x in text.split(',')]

    nums = list(range(256))

    currPos = 0
    for ss, l in enumerate(lengths):
        if l != 0:
            nums = nums[currPos:] + nums[:currPos]
            nums = nums[l - 1::-1] + nums[l:]
            nums = nums[-currPos:] + nums[:-currPos]

        currPos += ss + l
        currPos %= len(nums)

    part1 = nums[0] * nums[1]

    nums = list(range(256))
    
    ss = 0
    currPos = 0
    for round in range(64):
        for l in bs:
            if l != 0:
                nums = nums[currPos:] + nums[:currPos]
                nums = nums[l - 1::-1] + nums[l:]
                nums = nums[-currPos:] + nums[:-currPos]

            currPos += ss + l
            currPos %= len(nums)
            ss += 1

    denseHash = []
    for i, n in enumerate(nums):
        if i % 16 == 0:
            denseHash.append(0)

        denseHash[-1] = denseHash[-1] ^ n

    part2 = ''.join(['0' * (2 - len(hex(n)[2:])) + hex(n)[2:] for n in denseHash])

    if verbose:
        print(f"\nPart 1:\nProduct of first two numbers in list: {part1}\n\nPart 2:\nKnot Hash: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
