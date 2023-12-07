from time import perf_counter
from itertools import product

cardVals_P1 = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}
cardVals_P2 = {'A': 14, 'K': 13, 'Q': 12, 'J': 1, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}
handScores = [(1, 1, 1, 1, 1), (1, 1, 1, 2), (1, 2, 2), (1, 1, 3), (2, 3), (1, 4), (5,)]


def handsort_P1(hand):
    handScore = 0
    cardCounts = tuple(sorted([len([n for n in hand if n == c]) for c in set(hand)]))

    handScore += handScores.index(cardCounts) + 1

    for c in hand:
        handScore *= 100
        handScore += c

    return handScore


def handsort_P2(hand):
    handScore = 0
    cardCounts = [len([n for n in hand if n == c]) for c in set(hand) if c != 1]

    for p in product(range(len(cardCounts)), repeat=5-sum(cardCounts)):
        potHand = cardCounts[:]
        for ix in p:
            potHand[ix] += 1

        handScore = max(handScore, handScores.index(tuple(sorted(potHand))) + 1)

    if len(cardCounts) == 0:
        handScore = 7

    for c in hand:
        handScore *= 100
        handScore += c

    return handScore


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    hands_P1 = []
    bets_P1 = {}

    hands_P2 = []
    bets_P2 = {}

    for line in lines:
        hand, bet = line.split(' ')

        hand_P1 = tuple(cardVals_P1[c] for c in hand)
        hands_P1.append(hand_P1)
        bets_P1[hand_P1] = int(bet)

        hand_P2 = tuple(cardVals_P2[c] for c in hand)
        hands_P2.append(hand_P2)
        bets_P2[hand_P2] = int(bet)

    hands_P1.sort(key=handsort_P1)
    hands_P2.sort(key=handsort_P2)

    part1 = sum((i + 1) * bets_P1[h] for i, h in enumerate(hands_P1))
    part2 = sum((i + 1) * bets_P2[h] for i, h in enumerate(hands_P2))

    if verbose:
        print(f"\nPart 1:\n{part1}\n\nPart 2:\n{part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
