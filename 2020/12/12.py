import time

def manhatDist(p1, p2):
    return sum([abs(c1 - c2) for c1, c2 in zip(p1, p2)])

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    pos = (0, 0)
    facing = (1, 0)

    for line in data:
        if line[0] == 'N':
            pos = (pos[0], pos[1] - int(line[1:]))
        elif line[0] == 'E':
            pos = (pos[0] + int(line[1:]), pos[1])
        elif line[0] == 'S':
            pos = (pos[0], pos[1] + int(line[1:]))
        elif line[0] == 'W':
            pos = (pos[0] - int(line[1:]), pos[1])
        elif line[0] == 'F':
            pos = (pos[0] + facing[0] * int(line[1:]), pos[1] + facing[1] * int(line[1:]))
        else:
            for _ in range(int(line[1:]) // 90):
                facing = ((1 if line[0] == 'L' else -1) * facing[1], (1 if line[0] == 'R' else -1) * facing[0])

    print(f"\nPart 1:\nManhattan distance to final destination: {manhatDist(pos, (0, 0))}")

    pos = (0, 0)
    waypointOffset = (10, -1)

    for line in data:
        if line[0] == 'N':
            waypointOffset = (waypointOffset[0], waypointOffset[1] - int(line[1:]))
        elif line[0] == 'E':
            waypointOffset = (waypointOffset[0] + int(line[1:]), waypointOffset[1])
        elif line[0] == 'S':
            waypointOffset = (waypointOffset[0], waypointOffset[1] + int(line[1:]))
        elif line[0] == 'W':
            waypointOffset = (waypointOffset[0] - int(line[1:]), waypointOffset[1])
        elif line[0] == 'F':
            pos = (pos[0] + waypointOffset[0] * int(line[1:]), pos[1] + waypointOffset[1] * int(line[1:]))
        else:
            for _ in range(int(line[1:]) // 90):
                waypointOffset = ((1 if line[0] == 'L' else -1) * waypointOffset[1], (1 if line[0] == 'R' else -1) * waypointOffset[0])

    print(f"\nPart 2:\nManhattan distance to final destination: {manhatDist(pos, (0, 0))}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time}")
