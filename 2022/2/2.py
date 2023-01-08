from time import perf_counter

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n').split(' ') for line in f.readlines()]


    score = 0
    for p1, p2 in lines:
        played = [ord(p1) - ord('A'), ord(p2) - ord('X')]
        
        score += played[1] + 1
        if played[0] == played[1]:
            score += 3
        elif (played[1] - 1) % 3 == played[0]:
            score += 6    

    part1 = score

    score = 0
    for p1, p2 in lines:
        opp = ord(p1) - ord('A')
        if p2 == 'X':
            offset = 2
        elif p2 == 'Y':
            offset = 0
            score += 3
        else:
            offset = 1
            score += 6

        score += (opp + offset) % 3 + 1

    if verbose:
        print(f"\nPart 1:\nScore: {part1}\n\nPart 2:\nScore: {score}")

    return [part1, score]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
