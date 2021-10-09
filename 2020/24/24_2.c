#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#define dataLine 100
#define data "input.txt"
#define test "input1.txt"

typedef struct tile {
    bool state;
    int loc[2];
} Tile;

Tile *createTile(Tile *t, int *pos, bool side) {
    t->state = side;
    for (int i = 0; i < 2; i++) {
        t->loc[i] = pos[i];
    }

    return t;
}

void printTile(Tile *t) {
    printf("Tile %d,%d: Color: %s\n", t->loc[0], t->loc[1], (t->state) ? "black" : "white");
    return;
}


int *readData(int *results) {
	char textRead[dataLine], fileName[20];
	int *tiles = (int*)calloc(1, sizeof(int));

	#ifdef test
        strcpy(fileName, test);
	#endif // test

	#ifndef test
        strcpy(fileName, data);
	#endif // test

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return NULL;
    }

	while(fgets(textRead, dataLine, inFile)) {
        char *p = &textRead[0], past = 'e';
        int pos[2] = {0, 0};

        while (strlen(p) > 1) {
            switch (p[0]) {
                case 'n':
                    pos[0] += 2;
                    break;
                case 's':
                    pos[0] -= 2;
                    break;
                case 'e':
                    pos[1] += (past == 'e' || past == 'w') ? 2 : 1;
                    break;
                case 'w':
                    pos[1] -= (past == 'e' || past == 'w') ? 2 : 1;
                    break;
            }

            past = p[0];

            p++;
        }

        //x-Range
        if (pos[0] < results[2]) {
            results[2] = pos[0];
        } else if (pos[0] > results[3]) {
            results[3] = pos[0];
        }

        //y-Range
        if (pos[1] < results[4]) {
            results[4] = pos[1];
        } else if (pos[1] > results[5]) {
            results[5] = pos[1];
        }

        bool inTiles = false;
        Tile *t;

        for (int i = 0; i < results[1]; i++) {
            t = tiles[i];
            if (t->loc[0] == pos[0] && t->loc[1] == pos[1]) {
                inTiles = true;
                break;
            }
        }

        if (inTiles) {
            t->state = !t->state;
        } else {
            t = (Tile*)calloc(1, sizeof(Tile));
            t = createTile(t, &pos[0], true);
            tiles = realloc(tiles, (results[1] + 1) * sizeof(int));
            tiles[results[1]] = t;
            results[1]++;
        }
	}

	fclose(inFile);

	for (int i = 0; i < results[1]; i++) {
        Tile *t = tiles[i];
        printTile(t);
        if (t->state) {
            results[0]++;
        }
	}

	return tiles;
}

int countTiles(int *tiles, int numTiles) {
    int sum = 0;

    for (int i = 0; i < numTiles; i++) {
        Tile *t = tiles[i];
        if (t->state) {
            sum++;
        }
	}

    return sum;
}

int indexFrom2D(int *pos, int side) {
    return (pos[0] * side) + pos[1];
}

bool validPos(int x) {
    return (x % 2) == 0;
}

int countNeighbors(int *lut, int *pos, int xRange, int yRange) {
    int blCount = 0;

    for (int x = -1; x <= 1; x++) {
        for (int num = -1; num <= 1; num += 2) {
            int y = num * (x == 0) ? 2 : 1, tpos[2] = {pos[0] + x, pos[1] + y};

            if (tpos[0] < 0 || tpos[0] > xRange || tpos[1] < 0 || tpos[1] > yRange) {
                continue;
            }

            int index = indexFrom2D(&tpos[0], yRange);
            if (lut[index] != 0) {
                Tile *n = lut[index];
                blCount += (n->state) ? 1 : 0;
            }
        }
    }

    return blCount;
}

int main() {
    int results[6] = {0, 0, 0, 0, 0, 0}; // {# of black tiles, total tiles, xMin, xMax, yMin, yMax}
    int numTiles, day = 0, *tiles = readData(&results[0]);

    printf("\n");

    while (day <= 100) {
        printf("Day %d: %d\n", day, results[0]);


        // Set up LUT table
        numTiles = results[1];

        int mult = -1;
        for (int i = 2; i < 6; i++) {
            results[i] += mult * 2;
            mult *= -1;
        }

        int xRange = results[3] - results[2] + 1, yRange = results[5] - results[4] + 1, xOff = -results[2], yOff = -results[4];
        int *lut = (int*)calloc(xRange * yRange, sizeof(int));

        results[2] = 0, results[3] = xRange, results[4] = 0, results[5] = yRange;

        for (int i = 0; i < numTiles; i++) {
            Tile *t = tiles[i];
            t->loc[0] += xOff;
            t->loc[1] += yOff;

            int index = indexFrom2D(t->loc, yRange);
            lut[index] = t;
        }

        // Iteration of Game of Life Rules
        bool *newStates = (bool*)calloc(xRange * yRange, sizeof(bool));

        for (int j = 0; j <= xRange; j++) {
            for (int i = 0; i < yRange; i++) {
                int pos[2] = {j, i}, index = indexFrom2D(&pos[0], yRange), blCount = countNeighbors(lut, &pos[0], xRange, yRange);

                Tile *t = lut[index];

                if (t == 0 || !t->state) {
                    newStates[index] = (blCount == 2);
                } else {
                    newStates[index] = !(blCount == 0 || blCount > 2);
                }
            }
        }


        for (int j = 0; j <= xRange; j++) {
            for (int i = 0; i < yRange; i++) {
                int pos[2] = {j, i}, index = indexFrom2D(&pos[0], yRange);

                if (lut[index] == 0) {
                    if (newStates[index]) {
                        Tile *t = (Tile*)calloc(1, sizeof(Tile));
                        t = createTile(t, &pos[0], newStates[index]);

                        tiles = realloc(tiles, (numTiles + 1) * sizeof(int));
                        tiles[numTiles] = t;
                        lut[index] = t;

                        numTiles++;
                    }
                } else {
                    Tile *t = lut[index];
                    t->state = newStates[index];
                }
            }
        }


        day++;
        free(lut);
    }

    return 1;
}
