import time
import hashlib

def triple(h):
    for i in range(len(h) - 2):
        if len(set(h[i:i + 3])) == 1:
            return h[i]

    return ''

def quintuple(h):
    groups = ''
    for i in range(len(h) - 4):
        if len(set(h[i:i + 5])) == 1:
            groups += h[i]

    return groups

def stretchHash(salt, ix):
    result = hashlib.md5(f'{salt}{ix}'.encode()).hexdigest()
    for _ in range(2016):
        result = hashlib.md5(f'{result}'.encode()).hexdigest()

    return result

def main(verbose):
    data = "ihaygndm"
    i = 0
    keys = []
    posKeys = []
    trips = {}
    while len([k for k in keys if trips[k][1]]) < 64:
        for k in keys[::-1]:
            if k + 1000 < i and not trips[k][1]:
                keys.pop(keys.index(k))

        for k in posKeys[::-1]:
            if k + 1000 < i and not trips[k][1]:
                posKeys.pop(posKeys.index(k))
        
        while len(keys) < 64 and len(posKeys) != 0:
                keys.append(posKeys.pop(0))

        result = hashlib.md5(f'{data}{i}'.encode()).hexdigest()

        quint = quintuple(result)
        if len(quint) != 0:
            for pos, (char, used) in zip(trips.keys(), trips.values()):
                if not used:
                    if char in quint:
                        trips[pos][1] = True

        trip = triple(result)
        if len(trip) == 1:
            posKeys.append(i)
            trips[i] = [trip, False]

        i += 1

    part1 = keys[63]

    i = 0
    keys = []
    posKeys = []
    trips = {}
    while len([k for k in keys if trips[k][1]]) < 64:
        for k in keys[::-1]:
            if k + 1000 < i and not trips[k][1]:
                keys.pop(keys.index(k))

        for k in posKeys[::-1]:
            if k + 1000 < i and not trips[k][1]:
                posKeys.pop(posKeys.index(k))
        
        while len(keys) < 64 and len(posKeys) != 0:
                keys.append(posKeys.pop(0))

        result = stretchHash(data, i)

        quint = quintuple(result)
        if len(quint) != 0:
            for pos, (char, used) in zip(trips.keys(), trips.values()):
                if not used:
                    if char in quint:
                        trips[pos][1] = True

        trip = triple(result)
        if len(trip) == 1:
            posKeys.append(i)
            trips[i] = [trip, False]

        i += 1

    part2 = keys[63]

    if verbose:
        print(f"\nPart 1:\nIndex that produces 64th key: {part1}\n\nPart 2:\nIndex that produces 64th key: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
