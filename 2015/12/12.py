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

def main(verbose):
    with open("input.txt", encoding="UTF-8") as f:
        data = f.readline().strip('\n')

    data = json.loads(data)

    part1 = numSumP1(data)
    part2 = numSumP2(data)

    if verbose:
        print(f"\nPart 1:\nSum of numbers: {part1}\n\nPart 2:\nSum of numbers after ignoring red: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
