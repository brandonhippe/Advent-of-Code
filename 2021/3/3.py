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

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    gamma = ""
    epsilon = ""

    for i in range(len(lines[0]) - 1):
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

    print("Part 1:\nGamma: " + str(gamma) + "\nEpsilon: " + str(epsilon) + "\nPower Consumption: " + str(gamma * epsilon) + "\n")

    oxy = oxy_rating(lines, 0)
    co2 = co2_rating(lines, 0)
    
    print("Part 2:\nOxygen Generator Rating: " + str(oxy) + "\nCO2 Scrubber Rating: " + str(co2) + "\nLife Support Rating: " + str(oxy * co2) + "\n")

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
