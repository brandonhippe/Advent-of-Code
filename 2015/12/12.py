import time
import json

def numSumP1(data):
    if isinstance(data, dict):
        return sum(numSumP1(d) for d in data.values())
    elif isinstance(data, list):
        return sum(numSumP1(d) for d in data)
    elif isinstance(data, int):
        return data
    else:
        return 0

def numSumP2(data):
    if isinstance(data, dict):
        return sum(numSumP2(d) for d in data.values()) if "red" not in data.values() else 0
    elif isinstance(data, list):
        return sum(numSumP2(d) for d in data)
    elif isinstance(data, int):
        return data
    else:
        return 0

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = json.loads(f.readline().strip('\n'))

    print(f"\nPart 1:\nSum of numbers: {numSumP1(data)}")
    print(f"\nPart 2:\nSum of numbers after ignoring red: {numSumP2(data)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
