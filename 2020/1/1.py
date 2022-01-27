import time

def findSum(data, amt, val):
    elements = []

    if amt == 1:
        for d in data:
            if d == val:
                elements.append(d)
                break
    else:
        for d in data:
            if d < val:
                temp = data.copy()
                temp.remove(d)
                found = findSum(temp, amt - 1, val - d)
                if len(found) != 0:
                    elements = found.copy()                    
                    elements.append(d)
                    break

    return elements

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = f.readlines()

    for (i, line) in enumerate(lines):
        lines[i] = int(line)

    message = "Part 1: "
    product = 1
    nums = findSum(lines, 2, 2020)
    for (i, num) in enumerate(nums):
        product *= num
        message += str(num)
        if i + 1 != len(nums):
            message += " * "

    print(message + " = " + str(product))

    message = "Part 2: "
    product = 1
    nums = findSum(lines, 3, 2020)
    for (i, num) in enumerate(nums):
        product *= num
        message += str(num)
        if i + 1 != len(nums):
            message += " * "

    print(message + " = " + str(product))

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
