def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = f.readlines()

    for (i, line) in enumerate(lines):
        lines[i] = int(line)

    print("Part 1:")
    increased = 0
    for i in range(1, len(lines)):
        if lines[i] > lines[i - 1]:
            increased += 1

    print("Number of increases = " + str(increased))

    print("Part 2:")
    increased = 0
    for i in range(3, len(lines)):
        sums = [0] * 2
        frame1 = lines[i - 3:i]
        frame2 = lines[i - 2:i + 1]
        for j in range(3):
            sums[0] += frame1[j]
            sums[1] += frame2[j]

        if sums[1] > sums[0]:
            increased += 1

    print("Number of increases = " + str(increased))
main()
