class room:
    def __init__(self, index):
        self.index = index
        self.target = 10 ** self.index
        self.occupants = []

    def filled(self):
        for i in self.occupants:
            if i != self.target:
                return False

        return True

    def fillable(self):
        for i in self.occupants:
            if i != self.target and i != 0:
                return False
        
        return True

def energyUsed(startPos, endPos, rooms, hallway):
    # Pos index 0 ranges from 0-4, 0-3 are rooms and 4 is hallway
    if startPos[0] < 4:
        val = rooms[startPos[0]].occupants[startPos[1]]
        if val == rooms[startPos[0]].target and rooms[startPos[0]].fillable():
            return -1
    else:
        val = hallway[startPos[1]]

    if val == 0:
        return -1

    if endPos[0] < 4:
        if rooms[endPos[0]].occupants[endPos[1]] != 0:
            return -1
    else:
        if hallway[endPos[1]] != 0:
            return -1

    if startPos[0] < 4:
        if rooms[startPos[0]].filled():
            # Room is already in final state
            return -1

        if endPos[0] < 4:
            if val != rooms[endPos[0]].target:
                # Not the correct room
                return -1

            if not rooms[endPos[0]].fillable():
                # Target room isn't fillable yet
                return -1
    else:
        if endPos[0] < 4:
            if val != rooms[endPos[0]].target:
                # Not the correct room
                return -1

            if rooms[endPos[0]].fillable():
                endIndex = 0
                while endIndex < len(rooms[endPos[0]].occupants) and rooms[endPos[0]].occupants[endIndex] == 0:
                    endIndex += 1

                endIndex -= 1

                if endIndex != endPos[1]:
                    # Final position isn't all the way down
                    return -1
            else:
                # Target room isn't fillable yet
                return -1
        else:
            # Starting in hallway, finishing in hallway. Not valid
            return -1

    total = 0
    first = True
    while startPos != endPos:
        if startPos[0] < 4:
            if not first and rooms[startPos[0]].occupants[startPos[1]] != 0:
                return -1

            if startPos[0] != endPos[0]:
                if startPos[1] == 0:
                    startPos[1] = 2 + startPos[0] * 2
                    startPos[0] = 4
                else:
                    startPos[1] -= 1
            else:
                startPos[1] += 1
        else:
            if not first and hallway[startPos[1]] != 0:
                return -1

            if endPos[0] < 4:
                goalIndex = 2 + endPos[0] * 2
                if startPos[1] == goalIndex:
                    startPos[0] = endPos[0]
                    startPos[1] = 0
                    total += val
                    continue
            else:
                goalIndex = endPos[1]

            direction = (goalIndex - startPos[1]) // abs(goalIndex - startPos[1])
            startPos[1] += direction

        first = False
        total += val

    return total

def inFinal(rooms, hallway):
    if sum(hallway) != 0:
        return False

    for r in rooms:
        if not r.filled():
            return False

    return True

def lowestEnergy(rooms, hallway, allowance=float('inf')):
    if inFinal(rooms, hallway):
        return 0
    
    validPos = [[r, i] for i in range(len(rooms[0].occupants)) for r in range(4)] 
    for i in (0, 1, 3, 5, 7, 9, 10):
        validPos.append([4, i])

    validMoves = []
    for s in validPos:
        if (s[0] < 4 and rooms[s[0]].occupants[s[1]] != 0) or (s[0] == 4 and hallway[s[1]] != 0):
            for o in validPos:
                if o == s:
                    continue

                energyCount = energyUsed(s[:], o[:], rooms[:], hallway[:])
                if 0 < energyCount < allowance:
                    validMoves.append([s, o, energyCount])
    
    validMoves.sort(key=moveSort)
    
    lowEnergy = allowance
    for move in validMoves:
        newRooms = []
        for r in rooms:
            newRooms.append(room(r.index))
            newRooms[-1].occupants = r.occupants[:]

        newHall = hallway[:]
        start = move[0]
        end = move[1]
        
        if start[0] < 4:
            startVal = newRooms[start[0]].occupants[start[1]]
            newRooms[start[0]].occupants[start[1]] = 0
        else:
            startVal = newHall[start[1]]
            newHall[start[1]] = 0

        if end[0] < 4:
            newRooms[end[0]].occupants[end[1]] = startVal
        else:
            newHall[end[1]] = startVal
        
        energy = move[2] + lowestEnergy(newRooms, newHall, lowEnergy - move[2])
        if energy < lowEnergy:
            lowEnergy = energy
    
    return lowEnergy

def moveSort(e):
    return e[2]

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    roomsP1 = []
    roomsP2 = []
    for i in range(4):
        roomsP1.append(room(i))
        roomsP2.append(room(i))

    hallway = [0] * len(lines[1][1:-1])

    for line in lines[2:4]:
        line = line.split("#")
        while len(line[0]) == 0:
            line = line[1:-1]

        for (i, o) in enumerate(line):
            num = 10 ** (ord(o) - ord("A"))
            roomsP1[i].occupants.append(num)
            roomsP2[i].occupants.append(num)

    appendLines = ["#D#C#B#A#", "#D#B#A#C#"]
    for line in appendLines:
        line = line.split("#")
        while len(line[0]) == 0:
            line = line[1:-1]
        
        for (i, o) in enumerate(line):
            num = 10 ** (ord(o) - ord("A"))
            last = roomsP2[i].occupants[-1]
            roomsP2[i].occupants = roomsP2[i].occupants[:-1]
            roomsP2[i].occupants.append(num)
            roomsP2[i].occupants.append(last)
    
    print("\nPart 1:\nLowest Possible Energy: " + str(lowestEnergy(roomsP1, hallway)))
    print("\nPart 2:\nLowest Possible Energy: " + str(lowestEnergy(roomsP2, hallway)))

main()
