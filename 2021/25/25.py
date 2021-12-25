def increment(lines):
    newLines = []
    for line in lines:
        arr = line[:]
        newLines.append(arr)
    
    for (i, line) in enumerate(lines):
        for (j, l) in enumerate(line):
            if l == "<" and lines[i][j - 1] == ".":
                newLines[i][j] = "."
                newLines[i][j - 1] = "<"

    lines = []
    for line in newLines:
        arr = line[:]
        lines.append(arr)

    for (i, line) in enumerate(lines):
        for (j, l) in enumerate(line):
            if l == "^" and lines[i - 1][j] == ".":
                newLines[i][j] = "."
                newLines[i - 1][j] = "^"

    return newLines

def printCucumbers(lines):
    for i in range(len(lines) - 1, -1, -1):
        for j in range(len(lines[i]) - 1, -1, -1):
            c = "."
            if lines[i][j] == "<":
                c = ">"
            if lines [i][j] == "^":
                c = "v"

            print(c,end="")

        print(" ")

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    lines.reverse()
    for (i, line) in enumerate(lines):
        lines[i] = line[::-1]

    for (i, line) in enumerate(lines):
        newStr = ""
        for (j, l) in enumerate(line):
            if l == ">":
                newStr += "<"
            elif l == "v":
                newStr += "^"
            else:
                newStr += "."

        lines[i] = list(newStr)
    
    day = 0
    while True:
        #print("Day: " + str(day))
        #printCucumbers(lines)
        #print(" ")

        prevStr = []
        for line in lines:
            arr = line[:]
            prevStr.append(arr)
        
        lines = increment(lines)
        day += 1

        done = True
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                if lines[i][j] != prevStr[i][j]:
                    done = False
                    break

            if not done:
                break

        if done:
            break

    print("\nPart 1:\nFirst day no cucumbers move: " + str(day))    
    
main()
