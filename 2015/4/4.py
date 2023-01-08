import time
import hashlib

def main(verbose):
    data = 'bgvyzdsv'

    i = 0
    part1 = None
    part2 = None
    while part1 is None or part2 is None:
        result = hashlib.md5(f'{data}{i}'.encode()).hexdigest()
        if part1 is None and result[:5] == '00000':
            part1 = i

        if part2 is None and result[:6] == '000000':
            part2 = i

        i += 1

    if verbose:
        print(f"\nPart 1:\nFirst number to produce hash starting with at least 5 zeros: {part1}\n\nPart 2:\nFirst number to produce hash starting with at least 6 zeros: {part2}")

    return [part1, part2]
    

if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
