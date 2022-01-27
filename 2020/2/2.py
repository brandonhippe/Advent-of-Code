import time

class password:
    def __init__(self, data):
        self.min = int(data[0])
        self.max = int(data[1])
        self.letter = data[2].rstrip(data[2][-1])
        self.pw = data[3].rstrip(data[3][-1])
    
    def validP1(self):
        count = self.pw.count(self.letter)
        return count >= self.min and count <= self.max
    
    def validP2(self):
        return (self.pw[self.min - 1] == self.letter or self.pw[self.max - 1] == self.letter) and not (self.pw[self.min - 1] == self.letter and self.pw[self.max - 1] == self.letter)
    
def countValidP1(pwds):
    count = 0
    for pwd in pwds:
        count += 1 if pwd.validP1() else 0
    
    return count

def countValidP2(pwds):
    count = 0
    for pwd in pwds:
        count += 1 if pwd.validP2() else 0

    return count

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = f.readlines()

    pwds = []
    for line in lines:
        data = line.split('-', 1)
        temp = data[1].split(' ')
        data.remove(data[1])
        data.extend(temp)

        pwd = password(data)
        pwds.append(pwd)
    
    print('\nPart 1:\nValid Passwords: ' + str(countValidP1(pwds)))

    print('\nPart 2:\nValid Passwords: ' + str(countValidP2(pwds)))

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
