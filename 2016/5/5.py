import time
import hashlib

def main(verbose):
    data="abbhdwsy"
    i = 0
    passcodeP1 = ''
    passcodeP2 = [' '] * 8
    while len(passcodeP1) < 8 or ' ' in passcodeP2:
        result = hashlib.md5(f'{data}{i}'.encode()).hexdigest()
        if result[:5] == '00000':
            passcodeP1 += result[5]
            if result[5] in '01234567' and passcodeP2[int(result[5])] == ' ':
                passcodeP2[int(result[5])] = result[6]

        i += 1

    if verbose:
        print(f"\nPart 1:\nPasscode: {passcodeP1[:8]}\n\nPart 1:\nPasscode: {''.join(passcodeP2)}")

    return [passcodeP1[:8], ''.join(passcodeP2)]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
