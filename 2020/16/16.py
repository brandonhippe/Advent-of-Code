import time
import re

def clearFound(validFields, ix):
    if len(validFields[ix]) == 1:
        validFields[ix] = list(validFields[ix])[0]
        for i in range(len(validFields)):
            if i == ix or validFields[ix] not in validFields[i]:
                continue

            validFields[i].remove(validFields[ix])
            clearFound(validFields, i)

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    ranges = {}
    i = 0
    while len(data[i]) > 0:
        ranges[re.split(':', data[i])[0]] = [int(x) for x in re.findall('\d+', data[i])]
        i += 1

    i += 2
    mine = [int(x) for x in re.findall('\d+', data[i])]
    otherTickets = {tuple(int(x) for x in re.findall('\d+', line)) for line in data[i + 3:]}

    errorRate = 0
    for t in list(otherTickets):
        validTicket = True
        for n in t:
            valid = False
            for r in ranges.values():
                for i in range(0, len(r), 2):
                    if r[i] <= n <= r[i + 1]:
                        valid = True
                        break

                if valid:
                    break

            if not valid:
                errorRate += n
                validTicket = False

        if not validTicket:
            otherTickets.remove(t)

    print(f"\nPart 1:\nTicket scanning error rate: {errorRate}")

    validFields = {i: set(ranges.keys()) for i in range(len(ranges))}

    for t in list(otherTickets):
        for ix, n in enumerate(t):
            for k, r in zip(ranges.keys(), ranges.values()):
                valid = False
                for i in range(0, len(r), 2):
                    if r[i] <= n <= r[i + 1]:
                        valid = True
                        break
                
                if not valid and k in validFields[ix]:
                    validFields[ix].remove(k)
                    clearFound(validFields, ix)

    product = 1
    for i, n in enumerate(mine):
        if validFields[i].split(' ')[0] == 'departure':
            product *= n

    print(f"\nPart 2\nProduct of fields that start with departure: {product}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
