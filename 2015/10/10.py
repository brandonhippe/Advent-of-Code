import time

def main(verbose):
    data = '3113322113'
    for iteration in range(50):
        if iteration == 40:
            part1 = len(data)

        newData = ''
        i = 1
        d = data[0]
        count = 1
        while i < len(data):
            if data[i] != d:
                newData += f'{count}{d}'
                d = data[i]
                count = 1
            else:
                count += 1

            i += 1

        newData += f'{count}{d}'
        data = newData

    part2 = len(data)

    if verbose:
        print(f"\nPart 1:\nLength: {part1}\n\nPart 2:\nLength: {part2}")

    return [part1, part2]
    

if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
