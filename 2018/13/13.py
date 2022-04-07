import time

class Cart:
    def __init__(self, pos, char):
        self.pos = pos
        self.facing = {'>': complex(1), '<': complex(-1), 'v': complex(0, 1), '^': complex(0, -1)}[char]
        self.nextTurn = 0 # 0 for left, 1 for straight, 2 for right
        self.alive = True

    def __lt__(self, other):
        return (self.pos.imag < other.pos.imag) ^ (self.pos.real < other.pos.real)

    def rotate(self, POI):
        # Multiplying by j turns clockwise, multiplying by -j turns counterclockwise
        if POI.char == '+':
            if self.nextTurn % 2 == 0:
                self.facing *= complex(0, -1 if self.nextTurn == 0 else 1)

            self.nextTurn += 1
            self.nextTurn %= 3
        else:
            if (self.facing.imag == 0 and POI.char == '\\') or (self.facing.real == 0 and POI.char == '/'):
                self.facing *= complex(0, 1)
            else:
                self.facing *= complex(0, -1)

class POI:
    def __init__(self, pos, char):
        self.pos = pos
        self.char = char

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    carts = []
    tracks = {}
    POIs = {}
    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if l in '<>^v':
                carts.append(Cart(complex(x, y), l))
                tracks[complex(x, y)] = '-' if l in '<>' else '|'
            elif l in '/\+':
                POIs[complex(x, y)] = POI(complex(x, y), l)
            elif l in '-|':
                tracks[complex(x, y)] = l

    firstFound = False
    while len(carts) > 1:
        carts.sort()
        for cart in carts:
            if not cart.alive:
                continue

            cart.pos += cart.facing

            for cart2 in carts:
                if cart != cart2 and cart2.alive and cart.pos == cart2.pos:
                    cart.alive = False
                    cart2.alive = False
                    break

            if cart.alive and cart.pos in POIs:
                cart.rotate(POIs[cart.pos])

        if False in [c.alive for c in carts]:
            if not firstFound:
                firstFound = True
                for c in carts:
                    if not c.alive:
                        collision = c.pos
                        break

                print(f"\nPart 1:\nFirst collision occurs at position: {int(collision.real)}, {int(collision.imag)}")

            carts = [c for c in carts if c.alive]

    print(f"\nPart 2:\nPosition of final cart: {int(carts[0].pos.real)}, {int(carts[0].pos.imag)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
