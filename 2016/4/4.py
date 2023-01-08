import time
import re

class keyVal:
    def __init__(self, key, val):
        self.key = key
        self.val = val

    def __lt__(self, other):
        return self.val > other.val or (self.val == other.val and self.key < other.key)

class Room:
    def __init__(self, roomText):
        start, end = re.search('\d+', roomText).span()
        self.roomName = roomText[:start].replace('-', ' ')
        self.sectorID = int(roomText[start:end])
        self.checkSum = roomText[end+1:-1]
        self.real = True

    def valid(self):
        counts = {c: len([l for l in self.roomName if l == c]) for c in self.roomName if c != ' '}
        counts = [keyVal(k, counts[k]) for k in counts.keys()]
        
        counts.sort()
        self.real = ''.join(counts[i].key for i in range(5)) == self.checkSum

    def decrypt(self):
        decrypted = ''
        for c in self.roomName:
            num = ord(c)
            if c != ' ':
                num -= ord('a')
                num += self.sectorID
                num %= 26
                num += ord('a')

            decrypted += chr(num)

        return decrypted[:-1]

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        rooms = [Room(line.strip('\n')) for line in f.readlines()]

    sectorSums = 0
    for room in rooms:
        room.valid()
        if room.real:
            sectorSums += room.sectorID
            if room.decrypt() == "northpole object storage":
                part2 = room.sectorID

    part1 = sectorSums

    if verbose:
        print(f"\nPart 1:\nSum of sector IDs of real rooms: {part1}\n\nPart 2:\nSector ID of North Pole Object Storage: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
