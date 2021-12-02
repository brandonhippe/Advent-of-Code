def findPaths(data):
    if len(data) == 1:
        return 1
    
    count = 0
    i = 1
    while i < len(data) and data[i] - data[0] <= 3:
        count += findPaths(data[i:len(data)])
        i += 1

    return count

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = f.readlines()
    
    for (i, line) in enumerate(lines):
        lines[i] = int(line)

    lines.append(0)
    lines.sort()
    lines.append(lines[len(lines) - 1] + 3)

    print('\nPart 1:')
    ones = 0
    threes = 0
    for i in range (1, len(lines)):
        if lines[i] - lines[i - 1] == 1:
            ones += 1
        else:
            threes += 1

    print('Ones: ' + str(ones) + '\nThrees: ' + str(threes) + '\nProduct: ' + str(ones * threes) + '\n')


    print('Part 2:')
    paths = 1
    start = 0
    for i in range (1, len(lines) - 1):
        if lines[i + 1] - lines[i - 1] > 3:
            paths *= findPaths(lines[start:i + 1])
            start = i
    
    print('Number of paths: ' + str(paths) + '\n')

main()
    