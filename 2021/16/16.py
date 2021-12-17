class packet:
    def __init__(self, packetString):
        self.binary = packetString
        self.parsed = False
        self.subPackets = []

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
                    subPacket = packet(remainder)
                    self.subPackets.append(subPacket)
                    remainder = subPacket.parse()
                
                return remainder
            else:
                # Number of packets
                numPackets = int(self.binary[7:18], 2)
                remainder = self.binary[18:]
                
                for _ in range(numPackets):
                    subPacket = packet(remainder)
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
            sum = 0
            for sP in self.subPackets:
                sum += sP.eval()

            return sum
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

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [bin(int(line.strip(), 16)) for line in f.readlines()]

    packets = []
    for line in lines:
        line = line [2:]
        while len(line) % 4 != 0:
            line = '0' + line
        
        packets.append(packet(line))
        packets[-1].parse()
        print("Part 1:\nSum of Version Numbers: " + str(versionSums([packets[-1]])))    

    for p in packets:
        print("Part 2\nEvaulation of Packet: " + str(p.eval()))

main()
