import time
import re

class Node:
    def __init__(self, val):
        self.prev = None
        self.next = None
        self.val = val

class CircularLinkedList:
    def __init__(self) -> None:
        self.current = None

    def insert(self, node):
        if self.current == None:
            node.next = node
            node.prev = node
        else:
            node.prev = self.current
            node.next = self.current.next

            self.current.next.prev = node
            self.current.next = node

        self.current = node

    def remove(self):
        if self.current is not None:
            self.current.prev.next = self.current.next
            self.current.next.prev = self.current.prev
            returnNode = self.current
            self.current = self.current.next

            return returnNode

def main(filename):
    test = len(re.findall('\d+', filename)) == 1
    with open(filename, encoding='UTF-8') as f:
        players, marbles = [int(x) for x in re.findall('\d+', f.readline().strip())]
    
    circle = CircularLinkedList()
    circle.insert(Node(0))

    scores = [0] * players
    for marble in range(1, marbles + 1):
        if marble % 23 == 0:
            player = (marble - 1) % players
            scores[player] += marble

            for _ in range(7):
                circle.current = circle.current.prev

            scores[player] += circle.remove().val
            continue

        circle.current = circle.current.next
        circle.insert(Node(marble))

    print(f"\nPart 1:\nHigh score: {max(scores)}")

    for marble in range(marbles + 1, (marbles * 100) + 1):
        if marble % 23 == 0:
            player = (marble - 1) % players
            scores[player] += marble

            for _ in range(7):
                circle.current = circle.current.prev

            scores[player] += circle.remove().val
            continue

        circle.current = circle.current.next
        circle.insert(Node(marble))

    print(f"\nPart 2:\nHigh score: {max(scores)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
