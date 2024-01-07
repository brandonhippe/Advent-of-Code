#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#define fileName "input.txt"
#define dataLine 10

int numLines, iterations, xLen, yLen, zLen;
int dist(int x1, int y1, int z1, int x2, int y2, int z2);

typedef struct cube {
    int neighbors[27], x_, y_, z_, nIndex, state;
} Cube;

void printCube(struct cube *c, bool printNeighbors) {
    printf("Cube Addr: %d, X: %d, Y: %d, Z: %d\n", c, c->x_, c->y_, c->z_);
    //printf("%d\n", c->x_);
    //printf("%d\n", c->y_);
    //printf("%d\n", c->z_);
    //printf("%d\n", c->arr_);
    printf("State: %s\n", (c->state == 1) ? "true" : "false");

    if (printNeighbors) {
        printf("Neighbors:\n");
        for (int i = 0; i < 27; i++) {
            struct cube *c1 = c->neighbors[i];
            printf("Index: %d\n", i);
            if (c1) {
                printCube(c1, false);
            } else {
                printf("No neighbor.\n");
            }
        }

        printf("\n\n\n");
    }

    return;
}

void printCubes(int *cubes) {
    for (int z = 0; z < zLen; z++) {
        printf("Z: %d\n", z - iterations);
        for (int y = 0; y < yLen; y++) {
            for (int x = 0; x < xLen; x++) {
                for (int i = 0; i < xLen * yLen * zLen; i++) {
                    struct cube *c = cubes[i];
                    int cx = c->x_, cy = c->y_, cz = c->z_, cs = c->state;

                    if (dist(x - iterations, y - iterations, z - iterations, cx, cy, cz) == 0) {
                        printf("%s", (cs == 1) ? "#" : ".");
                        break;
                    }
                }
            }

            printf("\n");
        }

        printf("\n\n");
    }

    return;
}

struct cube *createCube(struct cube *c, int x, int y, int z) {
    c->x_ = x;
    c->y_ = y;
    c->z_ = z;
    c->state = 0;
    c->nIndex = 0;

    for (int i = 0; i < 27; i++) {
        c->neighbors[i] = 0;
    }

    return c;
}

int findLines() {
    int numLines = 0;
	char textRead[dataLine];

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        numLines++;
	}

	fclose(inFile);

	return numLines;
}

void readData(int *states) {
    int index = 0;
	char textRead[dataLine];

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	while(fgets(textRead, dataLine, inFile)) {
        for (int i = 0; i < numLines; i++) {
            char temp = textRead[i];
            if (temp != '\n') {
                int s = (temp == '#') ? 1 : 0;
                states[index] = s;
                index++;
            }
        }
	}

	fclose(inFile);

	return;
}

int dist(int x1, int y1, int z1, int x2, int y2, int z2) {
    return (pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2));
}

void assignNeighbors(int *cubes) {
    for (int i = 0; i < xLen * yLen * zLen - 1; i++) {
        struct cube *c = cubes[i];
        int cx = c->x_, cy = c->y_, cz = c->z_;

        for (int j = i + 1; j < xLen * yLen * zLen; j++) {
            struct cube *n = cubes[j];
            int nx = n->x_, ny = n->y_, nz = n->z_;

            if (dist(cx, cy, cz, nx, ny, nz) <= 3) {
                c->neighbors[c->nIndex] = n;
                n->neighbors[n->nIndex] = c;
                c->nIndex++;
                n->nIndex++;
            }
        }
    }

    return;
}

int main() {
    numLines = findLines();
    iterations = 6;
    xLen = numLines + 2 * iterations;
    yLen = numLines + 2 * iterations;
    zLen = 1 + 2 * iterations;

    if (numLines < 0) {
        printf("Error: Could not open file.\n");
        return -1;
    }

    printf("Starting!\n\n\n");

    printf("Creating cubes\n");
    int cubes[xLen * yLen * zLen], z = -iterations - 1, y = -iterations, x = -iterations;
    for (int i = 0; i < xLen * yLen * zLen; i++) {
        if (i % xLen == 0) {
            y++;
            x = -iterations;
        }
        if (i % (xLen * yLen) == 0) {
            z++;
            y = -iterations;
        }

        struct cube *c = (Cube*)calloc(1, sizeof(Cube));
        cubes[i] = createCube(c, x, y, z);

        x++;
    }

    printf("Reading initial state\n");
    int initial[numLines * numLines];
    readData(&initial[0]);

    y = -1;
    z = 0;
    for (int i = 0; i < numLines * numLines; i++) {
        x = i % numLines;
        if (x == 0) {
            y++;
        }

        for (int j = 0; j < xLen * yLen * zLen; j++) {
            struct cube *c = cubes[j];
            int cx = c->x_, cy = c->y_, cz = c->z_;
            if (dist(x, y, z, cx, cy, cz) == 0) {
                c->state = initial[i];
            }
        }
    }

    printf("Assigning neighboring cubes\n");
    assignNeighbors(&cubes[0]);

/*
    for (int i = 0; i < xLen * yLen * zLen; i++) {
        struct cube *c = cubes[i];
        printCube(c, true);
    }
*/



    int loops = 0;

    while (loops < iterations) {
        printf("Cycle #%d\n", loops + 1);
        int *nextStates = (int*)calloc(xLen * yLen * zLen, sizeof(int));

        for (int i = 0; i < xLen * yLen * zLen; i++) {
            struct cube *c = cubes[i], *c1;
            int neighborCount = 0, j = 0;

            c1 = c->neighbors[j];
            while (c1) {
                neighborCount += (c1->state) ? 1 : 0;
                j++;
                c1 = c->neighbors[j];
            }

            if (c->state == 0) {
                if (neighborCount == 3) {
                    nextStates[i] = 1;
                } else {
                    nextStates[i] = 0;
                }
            } else {
                if (neighborCount == 2 || neighborCount == 3) {
                    nextStates[i] = 1;
                } else {
                    nextStates[i] = 0;
                }
            }
        }

        for (int i = 0; i < xLen * yLen * zLen; i++) {
            struct cube *c = cubes[i];
            c->state = nextStates[i];
        }

        free(nextStates);
        loops++;
    }

/*
    for (int i = 0; i < xLen * yLen * zLen; i++) {
        struct cube *c = cubes[i];
        printCube(c, true);
    }
*/

    printf("Counting\n");
    int count = 0;

    for (int i = 0; i < xLen * yLen * zLen; i++) {
        struct cube *c = cubes[i];
        count += c->state;
    }

    printCubes(&cubes[0]);

    printf("\n\nCount = %d\n", count);


    return 1;
}
