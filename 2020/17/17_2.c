#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#define fileName "input.txt"
#define dataLine 10
#define iterations 6

int numLines, xLen, yLen, zLen, wLen;
int dist(int x1, int y1, int z1, int w1, int x2, int y2, int z2, int w2);

typedef struct cube {
    int neighbors[81], x_, y_, z_, w_, nIndex, state;
} Cube;

void printCube(struct cube *c, bool printNeighbors) {
    printf("Cube Addr: %d, X: %d, Y: %d, Z: %d, W: %d\n", c, c->x_, c->y_, c->z_, c->w_);
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
    for (int w = 0; w < wLen; w++) {
        for (int z = 0; z < zLen; z++) {
            printf("Z: %d, W: %d\n", z - iterations, w - iterations);
            for (int y = 0; y < yLen; y++) {
                for (int x = 0; x < xLen; x++) {
                    for (int i = 0; i < xLen * yLen * zLen * wLen; i++) {
                        struct cube *c = cubes[i];
                        int cx = c->x_, cy = c->y_, cz = c->z_, cw = c->w_, cs = c->state;

                        if (dist(x - iterations, y - iterations, z - iterations, w - iterations, cx, cy, cz, cw) == 0) {
                            printf("%s", (cs == 1) ? "#" : ".");
                            break;
                        }
                    }
                }

                printf("\n");
            }
        }

        printf("\n\n");
    }

    return;
}

struct cube *createCube(struct cube *c, int x, int y, int z, int w) {
    c->x_ = x;
    c->y_ = y;
    c->z_ = z;
    c->w_ = w;
    c->state = 0;
    c->nIndex = 0;

    for (int i = 0; i < 81; i++) {
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

int dist(int x1, int y1, int z1, int w1, int x2, int y2, int z2, int w2) {
    int d[4] = {abs(x1 - x2), abs(y1 - y2), abs(z1 - z2), abs(w1 - w2)}, maxD = 0;
    for (int i = 0; i < 4; i++) {
        if (d[i] > maxD) {
            maxD = d[i];
        }
    }

    return maxD;
}

void assignNeighbors(int *cubes) {
    for (int i = 0; i < xLen * yLen * zLen * wLen - 1; i++) {
        struct cube *c = cubes[i];
        int cx = c->x_, cy = c->y_, cz = c->z_, cw = c->w_;

        for (int j = i + 1; j < xLen * yLen * zLen * wLen; j++) {
            struct cube *n = cubes[j];
            int nx = n->x_, ny = n->y_, nz = n->z_, nw = n->w_;

            if (dist(cx, cy, cz, cw, nx, ny, nz, nw) <= 1) {
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
    xLen = numLines + 2 * iterations;
    yLen = numLines + 2 * iterations;
    zLen = 1 + 2 * iterations;
    wLen = 1 + 2 * iterations;

    if (numLines < 0) {
        printf("Error: Could not open file.\n");
        return -1;
    }

    printf("Starting!\n\n\n");

    printf("%d\n", xLen * yLen * zLen * wLen);

    printf("Creating cubes\n");
    int *cubes = (int *)calloc(xLen * yLen * zLen * wLen, sizeof(int));
    int w = -iterations - 1, z = -iterations, y = -iterations, x = -iterations;
    for (int i = 0; i < xLen * yLen * zLen * wLen; i++) {
        if (i % xLen == 0) {
            y++;
            x = -iterations;
        }
        if (i % (xLen * yLen) == 0) {
            z++;
            y = -iterations;
        }
        if (i % (xLen * yLen * zLen) == 0) {
            w++;
            z = -iterations;
        }

        struct cube *c = (Cube*)calloc(1, sizeof(Cube));
        cubes[i] = createCube(c, x, y, z, w);

        x++;
    }
/*
    for (int i = 0; i < xLen * yLen * zLen * wLen; i++) {
        struct cube *c = cubes[i];
        printCube(c, true);
    }
*/
    //printCubes(cubes);

    printf("Reading initial state\n");
    int initial[numLines * numLines];
    readData(&initial[0]);

    y = -1;
    z = 0;
    w = 0;
    for (int i = 0; i < numLines * numLines; i++) {
        x = i % numLines;
        if (x == 0) {
            y++;
        }

        for (int j = 0; j < xLen * yLen * zLen * wLen; j++) {
            struct cube *c = cubes[j];
            int cx = c->x_, cy = c->y_, cz = c->z_, cw = c->w_;
            if (dist(x, y, z, w, cx, cy, cz, cw) == 0) {
                c->state = initial[i];
            }
        }
    }

    //printCubes(cubes);

    printf("Assigning neighboring cubes\n");
    assignNeighbors(cubes);

/*
    for (int i = 0; i < xLen * yLen * zLen * wLen; i++) {
        struct cube *c = cubes[i];
        printCube(c, true);
    }
*/



    int loops = 0;

    while (loops < iterations) {
        printf("Cycle #%d\n", loops + 1);
        int *nextStates = (int*)calloc(xLen * yLen * zLen * wLen, sizeof(int));

        for (int i = 0; i < xLen * yLen * zLen * wLen; i++) {
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

        for (int i = 0; i < xLen * yLen * zLen * wLen; i++) {
            struct cube *c = cubes[i];
            c->state = nextStates[i];
        }

        free(nextStates);
        loops++;
    }

/*
    for (int i = 0; i < xLen * yLen * zLen * wLen; i++) {
        struct cube *c = cubes[i];
        printCube(c, true);
    }
*/

    printf("Counting\n");
    int count = 0;

    for (int i = 0; i < xLen * yLen * zLen * wLen; i++) {
        struct cube *c = cubes[i];
        count += c->state;
    }

    //printCubes(cubes);

    printf("\n\nCount = %d\n", count);


    return 1;
}
