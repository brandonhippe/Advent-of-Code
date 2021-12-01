def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = f.readlines()

    for (i, line) in enumerate(lines):
        lines[i] = int(line)

    message = "Part 1: "
    increased = 0
    for i in range(1, len(lines)):
        if lines[i] > lines[i - 1]:
            increased += 1

    print("Number of increases = " + str(increased))

main()
