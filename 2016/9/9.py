import time
import re

def determineLen(line, memo):
    length = len(line)
    marker = re.search('\([^(]*\)', line)
    while marker:
        start, end = marker.span()
        length -= end - start

        size, repeat = [int(x) for x in re.findall('\d+', marker.group())]
        repeat -= 1

        subLine = line[end:end+size]
        if subLine in memo:
            size = memo[subLine]
        else:
            size = determineLen(subLine, memo)
            memo[subLine] = size

        length += size * repeat

        line = line[:start] + line[end:]

        marker = re.search('\([^(]*\)', line)

    return length

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        line = f.readline().strip('\n')
    
    searchStart = 0
    marker = re.search('\([^(]*\)', line[searchStart:])
    while marker:
        start, end = marker.span()
        start += searchStart
        end += searchStart

        searchStart = start

        size, repeat = [int(x) for x in re.findall('\d+', marker.group())]
        searchStart += size * repeat
        repeat -= 1

        line = line[:start] + ''.join([line[end:end+size]] * repeat) + line[end:]

        marker = re.search('\([^(]*\)', line[searchStart:])

    print(f"\nPart 1:\nLength of decompressed file: {len(line)}")
    print(f"\nPart 2:\nLength of fully decompressed file: {determineLen(line, {})}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
