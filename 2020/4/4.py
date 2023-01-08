import time
import re


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    passports = []
    currPassport = {}
    for line in lines:
        if len(line) == 0:
            passports.append(currPassport)
            currPassport = {}
            continue

        for field in re.split(' ', line):
            k, v = re.split(':', field)
            currPassport[k] = v

    validP1, validP2 = 0, 0
    for i, p in enumerate(passports):
        if len(p) == 8 or (len(p) == 7 and 'cid' not in p):
            validP1 += 1

            try:
                if not (1920 <= int(p['byr']) <= 2002):
                    continue
                if not (2010 <= int(p['iyr']) <= 2020):
                    continue
                if not (2020 <= int(p['eyr']) <= 2030):
                    continue
                if ('cm' in p['hgt'] and not (150 <= int(p['hgt'][:-2]) <= 193)) or ('in' in p['hgt'] and not (59 <= int(p['hgt'][:-2]) <= 76)) or not ('cm' in p['hgt'] or 'in' in p['hgt']):
                    continue
                if not (p['hcl'][0] == '#' and int(p['hcl'][1:], 16) is not None):
                    continue
                if not (p['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']):
                    continue
                if not (len(p['pid']) == 9 and int(p['pid']) is not None):
                    continue

                validP2 += 1
            except ValueError:
                continue

    if verbose:
        print(f"\nPart 1:\nValid passports: {validP1}\nPart 2:\nValid passports with valid field data: {validP2}")

    return [validP1, validP2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
