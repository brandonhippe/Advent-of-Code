from time import perf_counter


class Packet:
    def __init__(self, packetString = "", div = False) -> None:
        self.packet = []
        self.div = div
        count = 0
        val = ""
        for i, c in enumerate(packetString):
            if c == '[':
                if count == 0:
                    start = i

                count += 1
            elif c == ']':
                count -= 1

                if count == 0:
                    self.packet.append(Packet(packetString[start + 1:i]))
            elif count == 0:
                if c == ',':
                    if len(val) != 0:
                        self.packet.append(int(val))
                        val = ""
                else:
                    val += c

        if len(val) != 0:
            self.packet.append(int(val))

    def __lt__(self, other):
        ix1, ix2 = 0, 0
        while ix1 < len(self.packet) and ix2 < len(other.packet):
            curr1, curr2 = self.packet[ix1], other.packet[ix2]
            if isinstance(curr1, int) and isinstance(curr2, int):
                if curr1 < curr2:
                    return True

                if curr1 > curr2:
                    return False
            elif isinstance(curr1, int) and isinstance(curr2, Packet):
                testPacket = Packet()
                testPacket.packet.append(curr1)
                if testPacket < curr2:
                    return True

                if testPacket > curr2:
                    return False
            elif isinstance(curr1, Packet) and isinstance(curr2, int):
                testPacket = Packet()
                testPacket.packet.append(curr2)
                if curr1 < testPacket:
                    return True

                if curr1 > testPacket:
                    return False
            else:
                if curr1 < curr2:
                    return True

                if curr1 > curr2:
                    return False

            ix1 += 1
            ix2 += 1

        return ix1 == len(self.packet) and ix2 != len(other.packet)


def main(verbose):
    with open("input.txt", encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    index = 0
    correctSum = 0
    packets = []
    for i in range(0, len(lines), 3):
        index += 1
        packet1 = Packet(lines[i][1:-1])
        packet2 = Packet(lines[i + 1][1:-1])

        packets.append(packet1)
        packets.append(packet2)

        if packet1 < packet2:
            correctSum += index

    packets.append(Packet("[[2]]", True))
    packets.append(Packet("[[6]]", True))

    packets.sort()
    product = 1
    for i, packet in enumerate(packets):
        if packet.div:
            product *= i + 1

    if verbose:
        print(f"\nPart 1:\nSum of indecies of packets in correct order: {correctSum}\n\nPart 2:\nProduct of divider packet indecies: {product}")

    return [correctSum, product]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")