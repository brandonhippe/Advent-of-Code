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
    double loc[2];
} Tile;

struct tile *createTile(struct tile *t, double *pos) {
    t->state = true;
    for (int i = 0; i < 2; i++) {
        t->loc[i] = pos[i];
    }

    return t;
}

void printTile(struct tile *t) {
    printf("Tile %.1f,%.1f: Color: %s\n", t->loc[0], t->loc[1], (t->state) ? "black" : "white");
    return;
}


int readData() {
	char textRead[dataLine], fileName[20];
	int sum = 0, *tiles = (int*)calloc(1, sizeof(int)), numTiles = 0;

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
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        char *p = &textRead[0], past = 'e';
        double pos[2] = {0, 0};

        while (strlen(p) > 1) {
            switch (p[0]) {
                case 'n':
                    pos[0]++;
                    break;
                case 's':
                    pos[0]--;
                    break;
                case 'e':
                    pos[1]+= (past == 'e' || past == 'w') ? 1 : 0.5;
                    break;
                case 'w':
                    pos[1]-= (past == 'e' || past == 'w') ? 1 : 0.5;
                    break;
            }

            past = p[0];

            p++;
        }

        bool inTiles = false;
        struct tile *t;

        for (int i = 0; i < numTiles; i++) {
            t = tiles[i];
            if (t->loc[0] == pos[0] && t->loc[1] == pos[1]) {
                inTiles = true;
                break;
            }
        }

        if (inTiles) {
            t->state = !t->state;
        } else {
            t = (struct tile*)calloc(1, sizeof(struct tile));
            t = createTile(t, &pos[0]);
            tiles = realloc(tiles, (numTiles + 1) * sizeof(int));
            tiles[numTiles] = t;
            numTiles++;
        }
	}

	fclose(inFile);

	for (int i = 0; i < numTiles; i++) {
        struct tile *t = tiles[i];
        printTile(t);
        if (t->state) {
            sum++;
        }
	}

	return sum;
}

int main() {
    printf("# of black tiles: %d\n", readData());

    return 1;
}
