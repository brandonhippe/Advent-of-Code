#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#include "../../Modules/input.h"
#include "../../Modules/set.h"
#define fileName "../../Inputs/2021_17.txt"


char *pointStr(int x, int y) {
    int sizex = ceil(log10(abs(x) + 1)), sizey = ceil(log10(abs(y) + 1));
    char *str = (char*)calloc(sizex + sizey + 2, sizeof(char));
    sprintf(str, "%d,%d", x, y);
    return str;
}


int triangleNum(int x) {
    return x * (x + 1) / 2;
}

int part1() {
    struct vector *input_data = singleLine(fileName, "=");

    int xMin, xMax, yMin, yMax;

    char *p = strtok(input_data->arr[1], "..");
    xMin = atoi(p);
    p = strtok(NULL, "..");
    xMax = atoi(p);

    p = strtok(input_data->arr[2], "..");
    yMin = atoi(p);
    p = strtok(NULL, "..");
    yMax = atoi(p);

    struct set *target = createSet(stringsize, copyElement);
    for (int y = yMin; y <= yMax; y++) {
        for (int x = xMin; x <= xMax; x++) {
            addSet(target, pointStr(x, y));
        }
    }

    int sxVel = 1;
    while (triangleNum(sxVel) < xMin) {
        sxVel++;
    }

    int landed = 0, highest = 0;
    for (int yV = yMin; yV <= 500; yV++) {
        for (int xV = sxVel; xV <= xMax; xV++) {
            int xVel = xV, yVel = yV, x = 0, y = 0, highestY = 0;

            while (x <= xMax && y >= yMin) {
                if (y > highestY) {
                    highestY = y;
                }

                if (inSet(target, pointStr(x, y))) {
                    landed++;

                    if (highestY > highest) {
                        highest = highestY;
                    }

                    break;
                }

                x += xVel;
                y += yVel;
                xVel--;
                yVel--;

                if (xVel < 0) {
                    xVel = 0;
                }
            }
        }
    }

    return highest;
}

int part2() {
    struct vector *input_data = singleLine(fileName, "=");

    int xMin, xMax, yMin, yMax;

    char *p = strtok(input_data->arr[1], "..");
    xMin = atoi(p);
    p = strtok(NULL, "..");
    xMax = atoi(p);

    p = strtok(input_data->arr[2], "..");
    yMin = atoi(p);
    p = strtok(NULL, "..");
    yMax = atoi(p);

    struct set *target = createSet(stringsize, copyElement);
    for (int y = yMin; y <= yMax; y++) {
        for (int x = xMin; x <= xMax; x++) {
            addSet(target, pointStr(x, y));
        }
    }

    int sxVel = 1;
    while (triangleNum(sxVel) < xMin) {
        sxVel++;
    }

    int landed = 0, highest = 0;
    for (int yV = yMin; yV <= 500; yV++) {
        for (int xV = sxVel; xV <= xMax; xV++) {
            int xVel = xV, yVel = yV, x = 0, y = 0, highestY = 0;

            while (x <= xMax && y >= yMin) {
                if (y > highestY) {
                    highestY = y;
                }

                if (inSet(target, pointStr(x, y))) {
                    landed++;

                    if (highestY > highest) {
                        highest = highestY;
                    }

                    break;
                }

                x += xVel;
                y += yVel;
                xVel--;
                yVel--;

                if (xVel < 0) {
                    xVel = 0;
                }
            }
        }
    }

    return landed;
}


int main () {
    clock_t t;
    t = clock(); 
    int p1 = part1();
    t = clock() - t; 
    double t_p1 = ((double)t) / CLOCKS_PER_SEC;
    printf("\nPart 1:\nHighest point reached: %d\nRan in %f seconds\n", p1, t_p1);

    t = clock(); 
    int p2 = part2();
    t = clock() - t;
    double t_p2 = ((double)t) / CLOCKS_PER_SEC;
    printf("\nPart 2:\nVelocites that land: %d\nRan in %f seconds\n", p2, t_p2);

    return 0;
}