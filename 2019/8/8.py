def zeroSort(e):
    return e[0]

def main():
    with open('input.txt', encoding='UTF-8') as f:
        data = [int(x) for x in f.readline()]

    data.reverse()
    width = 25
    height = 6

    numData = []
    for i in range(len(data) // (width * height)):
        layerData = [0] * 3
        arr = data[i * width * height:(i + 1) * width * height]
        for j in range(3):
            layerData[j] = arr.count(j)

        numData.append(layerData)

    numData.sort(key=zeroSort)
    print(f"\nPart 1:\n1's * 2's in layer with fewest 0's: {numData[0][1] * numData[0][2]}")

    visibleImg = [0] * (width * height)
    for layer in range(len(data) // (width * height)):
        arr = data[layer * width * height:(layer + 1) * width * height]
        for (i, num) in enumerate(arr):
            if num != 2:
                visibleImg[i] = num

    visibleImg.reverse()
    for y in range(height):
        for x in range(width):
            c = '#' if visibleImg[x + y * width] == 1 else ' '
            print(c,end='')

        print('')

main()
