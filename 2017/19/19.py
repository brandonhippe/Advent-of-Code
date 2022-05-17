import time

def pathFollow(start, lines):
    string = ''
    openList = [start]
    dir = (0, 1)
    steps = 0

    while len(openList) != 0:
        pos = openList.pop(0)
        if min(pos) < 0 or pos[0] >= len(lines[0]) or pos[1] >= len(lines):
            continue

        if lines[pos[1]][pos[0]] in '-|':
            openList.append(tuple([p + o for p, o in zip(pos, dir)]))
        elif lines[pos[1]][pos[0]] == '+':
            for pDir in [(dir[1], dir[0]), (dir[1], -dir[0]), (-dir[1], dir[0]), (-dir[1], -dir[0])]:
                newPos = tuple([p + o for p, o in zip(pos, pDir)])
                try:
                    if lines[newPos[1]][newPos[0]] != ' ':
                        dir = pDir
                        openList.append(newPos)
                        break
                except:
                    pass
        elif lines[pos[1]][pos[0]] != ' ':
            string += lines[pos[1]][pos[0]]
            openList.append(tuple([p + o for p, o in zip(pos, dir)]))

        steps += 1

    return (string, steps - 1)

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    corners = {}
    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if l == '+':
                corners[(x, y)] = []
            if y == 0 and l != ' ':
                start = (x, y)

    string, steps = pathFollow(start, lines)

    print(f"\nPart 1:\nLetters collected: {string}")
    print(f"\nPart 2:\nSteps: {steps}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
    