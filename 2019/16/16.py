import time

def FFTP1(data):
    basePattern = [0, 1, 0, -1]
    newData = []
    while len(newData) < len(data):
        val = 0
        for (i, d) in enumerate(data):
            repeat = len(newData) + 1
            index = i + 1
            index = index // repeat
            mult = basePattern[((i + 1) // repeat) % 4]
            val += mult * d
        
        newData.append(abs(val) % 10)

    return newData

def FFTP2(data):
    newData = [0]
    for d in data[::-1]:
        newData.append((d + newData[-1]) % 10)

    return newData[-1:0:-1]

def main():
    with open('input.txt', encoding='UTF-8') as f:
        data = f.readline().strip()

    dataP1 = [int(x) for x in data]
    for _ in range(100):
        dataP1 = FFTP1(dataP1)
        print(f"{_ + 1} %")
    
    print(f"\nPart 1:\nFirst 8 digits after 100 phases: {sum([val * 10 ** (7 - i) for (i, val) in enumerate(dataP1[:8])])}")

    dataP2 = data * 10000
    offset = int(dataP2[:7])
    dataP2 = [int(x) for x in dataP2[offset:]]

    for _ in range(100):
        dataP2 = FFTP2(dataP2)
        print(f"{_ + 1} %")
    
    print(f"\nPart 2:\nMessage: {sum([val * 10 ** (7 - i) for (i, val) in enumerate(dataP2[:8])])}")

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
