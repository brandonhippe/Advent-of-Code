import time

def triangle(n):
    return n * (n + 1) // 2

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]
    
    lines = lines[0].split("target area: x=")
    lines = lines[1:]
    lines = lines[0].split(", y=")
    lines = [line.split("..") for line in lines]

    data = []
    for line in lines:
        for l in line:
            data.append(int(l))

    yMax = float('-inf')

    xVel = 0
    
    while triangle(xVel) < data[0]:
        xVel += 1

    yVel = 0
    yVelMax = 0
    
    while yVel < 500:
        pos = [0, 0]
        vel = [xVel, yVel]
        maxY = 0

        while True:
            if pos[1] > maxY:
                maxY = pos[1]

            for (i, (p, v)) in enumerate(zip(pos, vel)):
                pos[i] = p + v
            
            if vel[0] != 0:
                vel[0] -= vel[0] // abs(vel[0])

            vel[1] -= 1

            if pos[0] > data[1] or pos[1] < data[2]:
                landed = False
                break

            if data[0] <= pos[0] <= data[1] and data[2] <= pos[1] <= data[3]:
                landed = True
                break

        if landed:
            if maxY > yMax:
                yMax = maxY

            yVelMax = yVel

        yVel += 1

    print("\nPart 1:\nMaximum Y Position on Landing Trajectory: " + str(yMax))

    trajectories = []
    xVelMin = xVel

    for yVel in range(data[2], yVelMax + 1):
        for xVel in range(xVelMin, data[1] + 1):
            pos = [0, 0]
            vel = [xVel, yVel]
            maxY = 0

            while True:
                if pos[1] > maxY:
                    maxY = pos[1]

                for (i, (p, v)) in enumerate(zip(pos, vel)):
                    pos[i] = p + v
                
                if vel[0] != 0:
                    vel[0] -= vel[0] // abs(vel[0])

                vel[1] -= 1

                if pos[0] > data[1] or pos[1] < data[2]:
                    landed = False
                    break

                if data[0] <= pos[0] <= data[1] and data[2] <= pos[1] <= data[3]:
                    landed = True
                    break

            if landed:
                trajectories.append([xVel, yVel])

    print("\nPart 2:\nNumber of Landing Trajectories: " + str(len(trajectories)))

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
