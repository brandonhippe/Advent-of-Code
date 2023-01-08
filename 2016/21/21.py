import time
import re

def scramble(password, lines):
    scramble = [c for c in password]
    for line in lines:
        if "swap" in line:
            if "position" in line:
                a, b = (int(x) for x in re.findall('\d+', line))
            else:
                a, b = (scramble.index(c[-1]) for c in re.findall('letter [a-z]', line))

            scramble[a], scramble[b] = scramble[b], scramble[a]
        elif "rotate" in line:
            if "right" in line:
                rot = list(int(x) for x in re.findall('\d+', line))[0]
            elif "left" in line:
                rot = -list(int(x) for x in re.findall('\d+', line))[0]
            else:
                rot = scramble.index(line[-1])
                rot += 1 if rot < 4 else 2

            rot %= len(scramble)

            scramble = scramble[-rot:] + scramble[:-rot]
        elif "reverse" in line:
            low, high = (int(x) for x in re.findall('\d+', line))
            scramble = scramble[:low] + list(reversed(scramble[low:high + 1])) + scramble[high + 1:]
        else:
            start, end = (int(x) for x in re.findall('\d+', line))
            if start > end:
                scramble = scramble[:end] + [scramble[start]] + scramble[end:start] + scramble[start + 1:]
            else:
                scramble = scramble[:start] + scramble[start + 1:end + 1] + [scramble[start]] + scramble[end + 1:]
    
    return ''.join(scramble)

def unscramble(scrambled, lines):
    password = [c for c in scrambled]
    for line in lines[::-1]:
        if "swap" in line:
            if "position" in line:
                a, b = (int(x) for x in re.findall('\d+', line))
            else:
                a, b = (password.index(c[-1]) for c in re.findall('letter [a-z]', line))

            password[a], password[b] = password[b], password[a]
        elif "rotate" in line:
            if "based" in line:
                i = 0
                while True:
                    scrambled = password[i:] + password[:i]
                    rot = scrambled.index(line[-1])
                    rot += 1 if rot < 4 else 2

                    rot %= len(scrambled)

                    scrambled = scrambled[-rot:] + scrambled[:-rot]

                    if scrambled == password:
                        break

                    i += 1

                password = password[i:] + password[:i]
                continue
            elif "right" in line:
                rot = list(int(x) for x in re.findall('\d+', line))[0]
            else:
                rot = -list(int(x) for x in re.findall('\d+', line))[0]

            rot *= -1
            rot %= len(password)

            password = password[-rot:] + password[:-rot]
        elif "reverse" in line:
            low, high = (int(x) for x in re.findall('\d+', line))
            password = password[:low] + list(reversed(password[low:high + 1])) + password[high + 1:]
        else:
            end, start = (int(x) for x in re.findall('\d+', line))
            if start > end:
                password = password[:end] + [password[start]] + password[end:start] + password[start + 1:]
            else:
                password = password[:start] + password[start + 1:end + 1] + [password[start]] + password[end + 1:]
    
    return ''.join(password)

def main(verbose):
    filename = "input.txt"
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    password = "abcde" + ("fgh" if '1' not in filename else "")
    scrambled = scramble(password, lines)
    part1 = scrambled

    if '1' not in filename:
        scrambled = "fbgdceah"

    password = unscramble(scrambled, lines)

    if verbose:
        print(f"\nPart 1:\nScrambled: {part1}\n\nPart 2:\nUnscrambled: {password}")

    return [part1, password]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
