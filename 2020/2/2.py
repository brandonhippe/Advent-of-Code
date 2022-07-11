from operator import xor
import time
import re

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    countP1, countP2 = 0, 0

    for line in lines:
        counts = [int(x) for x in re.findall('\d+', line)]
        c = re.findall('[a-z]:', line)[0][0]
        pwd = re.split(' ', line)[-1]

        if counts[0] <= len([a for a in pwd if a == c]) <= counts[1]:
            countP1 += 1

        if xor(pwd[counts[0] - 1] == c, pwd[counts[1] - 1] == c):
            countP2 += 1
    
    print(f"\nPart 1:\nValid Passwords: {countP1}")
    print(f"\nPart 2:\nValid Passwords: {countP2}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
