#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#define dataLine 100
#define data "input.txt"
//#define test "input1.txt"

typedef struct tile {
    bool state;
    int q, r, s; // Col, row, 3rd cube coordinate
} Tile;

Tile *createTile(Tile *t, int col, int row, bool side) {
    t->state = side;
    t->q = col;
    t->r = row;
    t->s = -t->q - t->r;

    return t;
}

void printTile(Tile *t) {
    printf("Tile %d,%d: Color: %s\n", t->q, t->r, (t->state) ? "black" : "white");
    return;
}

int countBlack(int *tiles, int numTiles) {
    int count = 0;

    for (int i = 0; i < numTiles; i++) {
        Tile *t = tiles[i];
        count += (int)(t->state);
    }

    return count;
}


int *readData(int *numT) {
	char textRead[dataLine], fileName[20];
	int *tiles = (int*)calloc(1, sizeof(int));
	int numTiles = 0;

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
        char *p = &textRead[0];
        int col = 0, row = 0;

        while (strlen(p) > 1) {
            switch (p[0]) {
                case 'n':
                    row++;
                    col += (int)(p[1] == 'e');
                    p++;
                    break;
                case 's':
                    row--;
                    col -= (int)(p[1] == 'w');
                    p++;
                    break;
                case 'e':
                    col++;
                    break;
                case 'w':
                    col--;
                    break;
            }

            p++;
        }

        bool inTiles = false;
        Tile *t;

        for (int i = 0; i < numTiles; i++) {
            t = tiles[i];
            if (t->q == col && t->r == row) {
                inTiles = true;
                break;
            }
        }

        if (inTiles) {
            t->state = !t->state;
        } else {
            t = (Tile*)calloc(1, sizeof(Tile));
            t = createTile(t, col, row, true);
            tiles = realloc(tiles, (numTiles + 1) * sizeof(int));
            tiles[numTiles] = t;
            numTiles++;
        }
	}

	fclose(inFile);

	*(numT) = numTiles;

	return tiles;
}


int main() {
    int numTiles;
    int *tiles = readData(&numTiles);

    printf("# of black tiles: %d\n", countBlack(tiles, numTiles));

    return 1;
}
