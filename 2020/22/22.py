import time

def combat(player1, player2, recursive = False):
    gameStates = set()

    while min(len(player1), len(player2)) > 0:
        if (tuple(player1), tuple(player2)) in gameStates:
            return [player1 + player2, []]

        gameStates.add((tuple(player1), tuple(player2)))

        if recursive and player1[0] < len(player1) and player2[0] < len(player2):
            win = len(combat(player1[1:1+player1[0]], player2[1:1+player2[0]], True)[0]) > 0
        else:
            win = player1[0] > player2[0]

        if win:
            player1 = player1[1:] + [player1[0], player2[0]]
            player2 = player2[1:]
        else:
            player2 = player2[1:] + [player2[0], player1[0]]
            player1 = player1[1:]

    return [player1, player2]

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    player1 = []
    player2 = []
    curr = player1
    for line in data:
        if len(line) == 0:
            curr = player2
            continue

        if line[0] == 'P':
            continue

        curr.append(int(line))

    p1, p2 = combat(player1[:], player2[:])
    winner = p1 if len(p1) != 0 else p2

    part1 = sum([n * (len(winner) - i) for i, n in enumerate(winner)])

    p1, p2 = combat(player1[:], player2[:], True)
    winner = p1 if len(p1) != 0 else p2
    part2 = sum([n * (len(winner) - i) for i, n in enumerate(winner)])

    if verbose:
        print(f"\nPart 1:\nWinner's score: {part1}\n\nPart 2:\nWinner's score: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
