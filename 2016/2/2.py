import time

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    keypad = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    moves = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}
    pos = (1, 1)
    code = 0
    for line in lines:
        for c in line:
            newPos = tuple(p + o for p, o in zip(pos, moves[c]))
            if 0 <= min(newPos) and len(keypad) > max(newPos):
                pos = newPos

        code *= 10
        code += keypad[pos[1]][pos[0]]

    part1 = code

    keypad = {(0, 0): '7', (1, 0): '8', (2, 0): '9', (-1, 0): '6', (-2, 0): '5', (0, 1): 'B', (0, 2): 'D', (0, -1): '3', (0, -2): '1', (-1, -1): '2', (1, -1): '4', (-1, 1): 'A', (1, 1): 'C'}

    moves = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}
    pos = (-2, 0)
    code = ''
    for line in lines:
        for c in line:
            newPos = tuple(p + o for p, o in zip(pos, moves[c]))
            if newPos in keypad:
                pos = newPos

        code += keypad[pos]

    part2 = code

    if verbose:
        print(f"\nPart 1:\nCode: {part1}\n\nPart 2:\nCode: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
