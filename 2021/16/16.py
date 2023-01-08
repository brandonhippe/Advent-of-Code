import time

class Packet:
    def __init__(self, packetString):
        self.binary = packetString
        self.parsed = False
        self.subPackets = []
        self.version = 0
        self.typeID = 0
        self.lengthType = 0
        self.value = 0

    def parse(self):
        if self.parsed:
            return

        self.parsed = True
        self.version = int(self.binary[:3], 2)
        self.typeID = int(self.binary[3:6], 2)

        if self.typeID == 4:
            # Literal Packet
            return self.parseLiteral(self.binary[6:])
        else:
            # Operator Packet
            self.subPackets = []
            self.lengthType = int(self.binary[6])

            if self.lengthType == 0:
                # Total Bits
                totalBits = int(self.binary[7:22], 2)
                remainder = self.binary[22:]

                while len(self.binary) - 22 - len(remainder) < totalBits:
                    subPacket = Packet(remainder)
                    self.subPackets.append(subPacket)
                    remainder = subPacket.parse()
                
                return remainder
            else:
                # Number of packets
                numPackets = int(self.binary[7:18], 2)
                remainder = self.binary[18:]
                
                for _ in range(numPackets):
                    subPacket = Packet(remainder)
                    self.subPackets.append(subPacket)
                    remainder = subPacket.parse()

                return remainder        

    def parseLiteral(self, literalString):
        i = 0
        number = ''
        while i < len(literalString):
            number += literalString[i + 1:i + 5]
            i += 5

            if literalString[i - 5] == '0':
                break            

        self.value = int(number, 2)
        return literalString[i:]

    def eval(self):
        if self.typeID == 0:
            # Sum Packet
            total = 0
            for sP in self.subPackets:
                total += sP.eval()

            return total
        if self.typeID == 1:
            # Product Packet
            product = 1
            for sP in self.subPackets:
                product *= sP.eval()

            return product
        if self.typeID == 2:
            # Minimum Packet
            minimum = float('inf')
            for sP in self.subPackets:
                num = sP.eval()
                if num < minimum:
                    minimum = num

            return minimum
        if self.typeID == 3:
            # Maximum Packet
            maximum = float('-inf')
            for sP in self.subPackets:
                num = sP.eval()
                if num > maximum:
                    maximum = num

            return maximum
        if self.typeID == 4:
            # Literal Packet
            return self.value
        if self.typeID == 5:
            # Greater Than Packet
            return int(self.subPackets[0].eval() > self.subPackets[1].eval())
        if self.typeID == 6:
            # Less Than Packet
            return int(self.subPackets[0].eval() < self.subPackets[1].eval())
        if self.typeID == 7:
            # Equal To Packet
            return int(self.subPackets[0].eval() == self.subPackets[1].eval())

def versionSums(packets):
    count = 0
    for p in packets:
        if not p.parsed:
            continue

        count += p.version
        count += versionSums(p.subPackets)
    
    return count

def main(verbose):
    with open('input.txt', encoding='UTF-8') as f:
        packet = Packet(bin(int(f.readline().strip(), 16))[2:])

    packet.parse()

    part1 = versionSums([packet])
    part2 = packet.eval()

    if verbose:
        print(f"\nPart 1:\nSum of Version Numbers: {part1}\n\nPart 2\nEvaulation of Packet: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
