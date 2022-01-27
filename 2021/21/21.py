from collections import Counter
import time

def stateString(stateArr):
    string = str(stateArr[0])
    for e in stateArr[1:]:
        string += ',' + str(e)

    return string

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    players = [0] * 2
    players[0] = int(lines[0].split(" starting position: ")[1])
    players[1] = int(lines[1].split(" starting position: ")[1])

    die = 1
    rolls = 0
    playersScores = [0] * 2
    playerIndex = 0

    while playersScores[0] < 1000 and playersScores[1] < 1000:
        for _ in range(3):
            players[playerIndex] += die
            players[playerIndex] = players[playerIndex] % 10
            if players[playerIndex] == 0:
                players[playerIndex] = 10

            die += 1
            rolls += 1
            if die > 100:
                die = die % 100

        playersScores[playerIndex] += players[playerIndex]
        
        playerIndex += 1
        playerIndex = playerIndex % 2
        
    print("\nPart 1:\nProduct of die rolls and losing score: " + str(rolls * playersScores[playerIndex]))

    states = {}
    states[stateString([int(lines[0].split(" starting position: ")[1]), int(lines[1].split(" starting position: ")[1]), 0, 0])] = 1
    playerIndex = 0
    playerWins = [0] * 2

    dice = list(Counter(
        i + j + k
        for i in range(1, 4)
        for j in range(1, 4)
        for k in range(1, 4)
    ).items())

    while len(states) != 0:
        newStates = {}
        for state in states:
            count = states[state]
            for (die, dieCount) in dice:
                stateArr = [int(x) for x in state.split(',')]
                stateArr[0] += die
                stateArr[0] = stateArr[0] % 10
                if stateArr[0] == 0:
                    stateArr[0] = 10

                stateArr[2] += stateArr[0]
                if stateArr[2] >= 21:
                    playerWins[0] += count * dieCount
                    continue
                
                tempState = stateArr[:]
                for (die2, die2Count) in dice:
                    stateArr = tempState[:]
                    stateArr[1] += die2
                    stateArr[1] = stateArr[1] % 10
                    if stateArr[1] == 0:
                        stateArr[1] = 10

                    stateArr[3] += stateArr[1]
                    if stateArr[3] >= 21:
                        playerWins[1] += count * dieCount * die2Count
                        continue

                    newState = stateString(stateArr)
                    if newState in newStates:
                        newStates[newState] += count * dieCount * die2Count
                    else:
                        newStates[newState] = count * dieCount * die2Count

        states = newStates

    playerWins.sort()
    print("\nPart 2:\nThe most universes won in is: " + str(playerWins[-1]))

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
