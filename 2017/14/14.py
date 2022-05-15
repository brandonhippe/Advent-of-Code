import time

def knotHash(bs):
    bs += [17, 31, 73, 47, 23]
    nums = list(range(256))
    
    ss = 0
    currPos = 0
    for _ in range(64):
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

    return ''.join(['0' * (2 - len(hex(n)[2:])) + hex(n)[2:] for n in denseHash])

def bfs(start, disks, visited):
    openList = [start]

    while len(openList) != 0:
        pos = openList.pop(0)

        for n in [tuple(p + o for p, o in zip(pos, offset)) for offset in [[0, 1], [0, -1], [1, 0], [-1, 0]]]:
            if not n in visited and 0 <= min(n) and 128 > max(n) and disks[n[1]][n[0]] == 1:
                openList.append(n)

        visited.add(pos)

def main(data='jxqlasbh'):
    disk = []
    for i in range(128):
        disk.append([int(x) for x in '0' * (128 - len(bin(int(knotHash([ord(c) for c in data + '-' + str(i)]), 16))[2:])) + bin(int(knotHash([ord(c) for c in data + '-' + str(i)]), 16))[2:]])

    print(f"\nPart 1:\nSquares used: {sum([sum(line) for line in disk])}")

    visited = set()
    regions = 0
    for y, line in enumerate(disk):
        for x, s in enumerate(line):
            if s == 1 and (x, y) not in visited:
                regions += 1
                bfs((x, y), disk, visited)

    print(f"\nPart 2:\nNumber of regions: {regions}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
