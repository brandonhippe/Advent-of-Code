import time

def modMultInv(n, m):
    return pow(n, m - 2, m)

def main(verbose):
    with open('input.txt', encoding='UTF-8') as f:
        lines = [[x for x in line.strip('\n').split(' ')] for line in f.readlines()]

    a, b = [1, 0]
    deckLen = 10007
    
    for line in lines:
        if 'stack' in line:
            c, d = [-1, -1]
        elif 'increment' in line:
            c, d = [int(line[-1]), 0]
        else:
            c, d = [1, -int(line[-1])]

        # Composition of linear shuffles
        a, b = [(a * c) % deckLen, (b * c + d) % deckLen]

    part1 = (2019 * a + b) % deckLen

    a, b = [1, 0]
    deckLen = 119315717514047
    shuffles = 101741582076661
    
    for line in lines:
        if 'stack' in line:
            c, d = [-1, -1]
        elif 'increment' in line:
            c, d = [int(line[-1]), 0]
        else:
            c, d = [1, -int(line[-1])]

        # Composition of linear shuffles
        a, b = [(a * c) % deckLen, (b * c + d) % deckLen]

    # Calculate coeffiecents a, b after applying shuffle sequence for number of shuffles, done by modular exponentiation (repeated composition into itself)
    b = b * (1 - pow(a, shuffles, deckLen)) * modMultInv(1 - a, deckLen)
    a = pow(a, shuffles, deckLen)

    part2 = ((2020 - b) * modMultInv(a, deckLen)) % deckLen

    if verbose:
        print(f"\nPart 1:\nPosition of card 2019: {part1}\n\nPart 2:\nCard at position 2020: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
