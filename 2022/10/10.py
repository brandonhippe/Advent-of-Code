from time import perf_counter


def main(verbose):
    with open("input.txt", encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    x = 1
    cycles = 0

    signalStrength = 0
    for line in lines:
        if line == "noop":
            cycles += 1
            if cycles in [20, 60, 100, 140, 180, 220]:
                signalStrength += x * cycles
        else:
            cycles += 1
            if cycles in [20, 60, 100, 140, 180, 220]:
                signalStrength += x * cycles
            
            cycles += 1
            if cycles in [20, 60, 100, 140, 180, 220]:
                signalStrength += x * cycles

            x += int(line.split(' ')[1])

    if verbose:
        print(f"\nPart 1:\nSum of signal strengths: {signalStrength}\n\nPart 2:\nText on CRT:")

        x = 1
        cycles = 0

        for line in lines:
            if cycles % 40 == 0:
                print("")

            if abs(x - (cycles % 40)) <= 1:
                print("#", end='')
            else:
                print(' ', end='')

            cycles += 1

            if line != "noop":
                if cycles % 40 == 0:
                    print("")

                if abs(x - (cycles % 40)) <= 1:
                    print("#", end='')
                else:
                    print(' ', end='')

                x += int(line.split(' ')[1])

                cycles += 1

        print("")

    return [signalStrength, None]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")