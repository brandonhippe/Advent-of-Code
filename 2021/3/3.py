import time

def oxy_rating(data, bit):
    if len(data) == 1:
        return int(data[0], 2)

    newData = []
    counts = [0] * 2
    for line in data:
        counts[int(line[bit])] += 1

    search = ''
    if counts[0] > counts[1]:
        search = '0'
    else:
        search = '1'
    
    for line in data:
        if line[bit] == search:
            newData.append(line)

    return oxy_rating(newData, bit + 1)

def co2_rating(data, bit):
    if len(data) == 1:
        return int(data[0], 2)

    newData = []
    counts = [0] * 2
    for line in data:
        counts[int(line[bit])] += 1

    search = ''
    if counts[0] <= counts[1]:
        search = '0'
    else:
        search = '1'
    
    for line in data:
        if line[bit] == search:
            newData.append(line)

    return co2_rating(newData, bit + 1)

def main(verbose):
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    gamma = ""
    epsilon = ""

    for i in range(len(lines[0])):
        counts = [0] * 2
        for line in lines:
            counts[int(line[i])] += 1
        
        if counts[0] > counts[1]:
            gamma = gamma + '0'
            epsilon = epsilon + '1'
        else:
            gamma = gamma + '1'
            epsilon = epsilon + '0'

    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)

    oxy = oxy_rating(lines, 0)
    co2 = co2_rating(lines, 0)
    
    if verbose:
        print(f"Part 1:\nPower Consumption: {gamma * epsilon}\n\nPart 2:\nLife Support Rating: {oxy * co2}")

    return [gamma * epsilon, oxy * co2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
