from time import perf_counter
import re
from collections import defaultdict


def getCards(c, cards, cardsGiven):
    if c in cardsGiven:
        return cardsGiven[c]
    
    cardsGiven[c] += sum(getCards(n, cards, cardsGiven) for n in cards[c])
    
    return cardsGiven[c]


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    part1 = 0
    for line in lines:
        line = line.split(': ')[1]
        winning, have = line.split(' | ')

        winning = set(int(n) for n in re.findall('\d+', winning))
        have = set(int(n) for n in re.findall('\d+', have))

        match = winning.intersection(have)
        
        if len(match) > 0:
            part1 += 2 ** (len(match) - 1)

    cards = {}
    for line in lines:
        card, info = line.split(': ')
        winning, have = info.split(' | ')

        card = int(re.findall('\d+', card)[0])
        winning = set(int(n) for n in re.findall('\d+', winning))
        have = set(int(n) for n in re.findall('\d+', have))

        match = winning.intersection(have)
        cards[card] = list(range(card + 1, card + len(match) + 1))

    part2 = 0
    cardsGiven = defaultdict(lambda: 1)
    for c in cards.keys():
        part2 += getCards(c, cards, cardsGiven)

    if verbose:
        print(f"\nPart 1:\nScore of cards: {part1}\n\nPart 2:\nCards recieved: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
