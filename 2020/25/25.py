import time

data = [1327981, 2822615]
# data = [5764801, 17807724]

def loopSize(index):
    val = 1
    subject = 7
    count = 0

    while val != data[index]:
        val *= subject
        val = val % 20201227
        count += 1

    return count

def main():
    loops = [0] * len(data)
    for i in range(len(data)):
        loops[i] = loopSize(i)
    
    val = 1
    subject = data[1]
    for i in range(loops[0]):
        val *= subject
        val = val % 20201227
    
    print("Encryption key: " + str(val))

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
