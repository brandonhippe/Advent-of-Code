#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#define fileName "input.txt"
#define testFile "input1.txt"
#define outputFile "input2.txt"
#define monsterFile "monster.txt"
#define monsterLen 21
#define test false

int size, side, dataLine;


typedef struct tile {
    int id, match[8], type, sides[4], loc;
    char image[101];
} Tile;

struct tile *createTile(struct tile *t, int id_, char *img) {
    t->id = id_;
    t->type = 0;
    t->loc = -1;
    strcpy(t->image, img);

    for (int i = 0; i < 8; i++) {
        t->match[i] = 0;
        t->sides[i / 2] = 0;
    }

    return t;
}

void printTile(struct tile *t) {
    printf("Id: %d\n", t->id);
    char *img = (char*)calloc((dataLine * dataLine) + 1, sizeof(char)), *p = img, *temp = (char*)calloc(dataLine + 1, sizeof(char));
    strcpy(img, t->image);

    while (p[0] != '\n') {
        strncpy(temp, p, dataLine);
        printf("%s\n", temp);
        p += dataLine * sizeof(char);
    }

    printf("\nMatches in each orientation:");
    for (int i = 0; i < 8; i++) {
        printf("\n%d", t->match[i]);
    }


    printf("\n");
    //printf("Flip: %d ", t->flipped);
    printf("%s", t->type == 2 ? "***CORNER***" : t->type == 1 ? "***EDGE***" : "***CENTER***");
    printf("\n\n");

    return;
}

int findLines() {
	int numLines = 0;
	char textRead[dataLine + 2];

	// Open the file
	FILE *inFile = fopen((test) ? testFile : fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine + 2, inFile)) {
        if (textRead[1] == 'i') {
            ++numLines;
        }
	}

	fclose(inFile);

	return numLines;
}

void readData(int *tiles) {
    int tNum = -1, id_;
	char textRead[dataLine + 2], *img = (char*)calloc((dataLine * dataLine) + 2, sizeof(char));

	// Open the file
	FILE *inFile = fopen((test) ? testFile : fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return;
    }

	while(fgets(textRead, dataLine + 2, inFile)) {
        if (textRead[0] == 'T') {
            if (tNum >= 0) {
                struct tile *t = (struct tile*)calloc(1, sizeof(struct tile));
                t = createTile(t, id_, img);
                tiles[tNum] = t;
            }

            char *p = strchr(textRead, ' ');
            id_ = atoi(p);
            ++tNum;
            strcpy(img, "");
        } else {
            strncat(img, textRead, dataLine);
        }
	}

	fclose(inFile);

	return;
}

char *flip(char *str, int slen) {
    char *res = (char*)calloc(strlen(str) + 1, sizeof(char)), *p = str + ((slen - 1) * slen);

    while (p >= str) {
        strncat(res, p, slen);
        p -= slen;
    }

    strcat(res, "\n");

    return res;
}

char *rotate(char *str, int slen) {
    char *res = (char*)calloc(strlen(str) + 1, sizeof(char)), *p;
    int index = 0, i = 0;

    while (index < slen) {
        while (i < slen * slen) {
            p = str + i;
            if (i % slen == index) {
                strncat(res, p, 1);
            }
            i++;
        }

        i = 0;
        index++;
    }

    strcat(res, "\n");

    return res;
}

void shiftArr(int *arr, int len, int amt) {
    while (amt > 0) {
        int temp = arr[0];

        for (int i = 0; i < len - 1; i++) {
            arr[i] = arr[i + 1];
        }

        arr[len - 1] = temp;

        amt--;
    }

    return;
}

int indexFrom2d(int x, int y) {
    return (y * side) + x;
}

void matchSides(int *tiles) {
    for (int n = 0; n < size; n++) {
        struct tile *t = tiles[n];

        for (int i = 0; i < 8; i++) {
           for (int j = 0; j < size; j++) {
                if (n == j) {
                    continue;
                }
                struct tile *t1 = tiles[j];

                for (int k = 0; k < 8; k++) {
                    if (strncmp(t->image, t1->image, dataLine) == 0) {
                        t->match[i]++;
                    }

                    strcpy(t1->image, (k % 2 == 0) ? flip(t1->image, dataLine) : rotate(t1->image, dataLine));
                }
            }

            strcpy(t->image, (i % 2 == 0) ? flip(t->image, dataLine) : rotate(t->image, dataLine));
        }
    }

    return;
}

void genMatches(struct tile *t, int *tiles, int tloc) {
    t->loc = tloc;

    if ((t->match[1] == 1 || t->match[4] == 1) && t->sides[2] == 0) {
        // Match bottom

        int search = tloc + side;

        bool found = false;
        for (int i = 0; i < size; i++) {
            struct tile *t1 = tiles[i];
            if (t1->loc == search) {
                t->sides[2] = t1;
                t1->sides[0] = t;
                found = true;
            }
        }

        if (!found) {
            char *endT = (char*)calloc(dataLine + 1, sizeof(char));
            strncpy(endT, t->image + dataLine * (dataLine - 1), dataLine);

            for (int i = 0; i < size; i++) {
                if (tiles[i] == t) {
                    continue;
                }

                struct tile *t1 = tiles[i];

                for (int or = 0; or < 8; or++) {
                    char *startT1 = (char*)calloc(dataLine + 1, sizeof(char));
                    strncpy(startT1, t1->image, dataLine);

                    if (strcmp(endT, startT1) == 0) {
                        t->sides[2] = t1;
                        t1->sides[0] = t;
                        genMatches(t1, tiles, search);

                        found = true;
                        break;
                    }

                    strcpy(t1->image, (or % 2 == 0) ? flip(t1->image, dataLine) : rotate(t1->image, dataLine));
                    shiftArr(t1->match, 8, 1);
                    shiftArr(t1->sides, 4, or % 2);
                }

                if (found) {
                    break;
                }
            }
        }
    }

    if ((t->match[3] == 1 || t->match[6] == 1) && t->sides[1] == 0) {
        // Match right

        int search = tloc + 1;

        bool found = false;
        for (int i = 0; i < size; i++) {
            struct tile *t1 = tiles[i];
            if (t1->loc == search) {
                t->sides[2] = t1;
                t1->sides[0] = t;
                found = true;
            }
        }

        if (!found) {
            char *endT = (char*)calloc(dataLine + 1, sizeof(char));
            for (int i = 0; i < dataLine; i++) {
                strncat(endT, t->image + i * dataLine + 9, 1);
            }

            for (int i = 0; i < size; i++) {
                if (tiles[i] == t) {
                    continue;
                }

                struct tile *t1 = tiles[i];

                for (int or = 0; or < 8; or++) {
                    char *startT1 = (char*)calloc(dataLine + 1, sizeof(char));
                    for (int i = 0; i < dataLine; i++) {
                        strncat(startT1, t1->image + i * dataLine, 1);
                    }

                    if (strcmp(endT, startT1) == 0) {
                        t->sides[1] = t1;
                        t1->sides[3] = t;
                        genMatches(t1, tiles, search);

                        found = true;
                        break;
                    }

                    strcpy(t1->image, (or % 2 == 0) ? flip(t1->image, dataLine) : rotate(t1->image, dataLine));
                    shiftArr(t1->match, 8, 1);
                    shiftArr(t1->sides, 4, or % 2);
                }

                if (found) {
                    break;
                }
            }
        }
    }

    return;
}

void formatImg(struct tile *s, char *img) {
    struct tile *curr = 0, *next = s;

    do {
        for (int line = 1; line < 9; line++) {
            do {
                if (curr == 0) {
                    curr = next;
                } else {
                    curr = curr->sides[1];
                }

                char *temp = curr->image + line * dataLine + 1, *p = (char*)calloc(9, sizeof(char));
                strncat(img, temp, 8);
                strncpy(p, temp, 8);
            } while (curr->sides[1] != 0);

            while (curr->sides[3] != 0) {
                curr = curr->sides[3];
            }

            next = curr;
            curr = 0;
        }

        next = next->sides[2];
    } while (next);

    return;
}

void genMonster(char *monster) {
    char textRead[monsterLen + 1];

	// Open the file
	FILE *inFile = fopen(monsterFile, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return;
    }

	while(fgets(textRead, dataLine, inFile)) {
        strncat(monster, textRead, monsterLen - 1);
	}

	fclose(inFile);

	return;
}

void writeFile(char *img) {
    char *p = img;
	FILE *outFile = NULL;

	outFile = fopen(outputFile, "w");

	// Check if file could be opened
	if (outFile == NULL) {
		printf("Couldn't write to file.\n");
		return;
	}

	while (p < img + strlen(img)) {
        char *temp = (char*)calloc(8 * side + 1, sizeof(char));
        strncpy(temp, p, 8 * side);
        fprintf(outFile, "%s\n", temp);
        p += 8 * side;
	}

	// Close file
	fclose(outFile);

	return;
}

void readImg(char *img) {
	char textRead[dataLine];

	// Open the file
	FILE *inFile = fopen(outputFile, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return;
    }

	while(fgets(textRead, dataLine, inFile)) {
        strncat(img, textRead, side);
	}

	fclose(inFile);

	return;
}

int roughness() {
    char *img = (char*)calloc(dataLine * dataLine, sizeof(char));
    readImg(img);

    char *monster = (char*)calloc(monsterLen * 3 + 1, sizeof(char));
    genMonster(monster);

    for (int or = 0; or < 8; or++) {
        for (int i = 0; i < side - 2; i++) {
            for (int j = 0; j <= side - monsterLen + 1; j++) {
                int start = i * side + j, mIndex = 0;

                bool found = true;
                while (monster[mIndex]) {
                    if (monster[mIndex] == '#' && img[start + side * (mIndex / (monsterLen - 1)) + (mIndex % (monsterLen - 1))] == '.') {
                        found = false;
                        break;
                    }

                    mIndex++;
                }

                if (found) {
                    mIndex = 0;
                    while (monster[mIndex]) {
                        if (monster[mIndex] == '#') {
                            img[start + side * (mIndex / (monsterLen - 1)) + (mIndex % (monsterLen - 1))] = 'O';
                        }

                        mIndex++;
                    }
                }
            }
        }

        strcpy(img, (or % 2 == 0) ? flip(img, side) : rotate(img, side));
    }

    printf("\n\n\nMonsters found in the water:\n");

    char *p = img;
    for (int i = 0; i < side; i++) {
        char *temp = (char*)calloc(dataLine, sizeof(char));
        strncpy(temp, p, side);
        p += side;

        printf("%s\n", temp);
    }

    int i = 0, count = 0;
    while (img[i]) {
        count += (img[i] == '#') ? 1 : 0;
        i++;
    }

    return count;
}

int main() {
    dataLine = 10;
    size = findLines(), side = sqrt(size);
    printf("Number of tiles: %d\n\n", size);


    int *tiles = (int*)calloc(size, sizeof(struct tile));
    readData(tiles);


    matchSides(tiles);
    for (int i = 0; i < size; i++) {
        struct tile *t = tiles[i];
        int zeros = 0;

        for (int j = 0; j < 8; j++) {
            zeros += (t->match[j] == 0) ? 1 : 0;
        }

        t->type = zeros / 2;
    }

    unsigned long long int product = 1, corners = 0;
    for (int i = 0; i < size; i++) {
        struct tile *t = tiles[i];
        printTile(t);

        if (t->type == 2) {
            product *= t->id;
            corners++;
        }
    }


/*
    for (int i = 0; i < side; i++) {
        for (int j = 0; j < side; j++) {
            for (int k = 0; k < size; k++) {
                int index = indexFrom2d(j, i);
                if (k == index) {
                    struct tile *t = tiles[index];
                    printf(" %d ", t->id);
                }
            }
        }
        printf("\n");
    }
*/

    printf("Corners: %d\nProduct of corner IDs: %llu\n\n", corners, product);

    struct tile *c0;

    for (int i = 0; i < size; i++) {
        struct tile *t = tiles[i];
        if (t->type == 2) {
            for (int or = 0; or < 8 && t->match[1] + t->match[3] + t->match[4] + t->match[6] != 4; or++) {
                strcpy(t->image, (or % 2 == 0) ? flip(t->image, dataLine) : rotate(t->image, dataLine));
                shiftArr(t->match, 8, 1);
            }

            c0 = t;
            break;
        }
    }

    genMatches(c0, tiles, 0);

    struct tile *curr = 0, *next = c0;

    do {
        if (curr != 0) {
            next = curr->sides[2];
            curr = 0;
        }

        do {
            if (curr == 0) {
                curr = next;
            } else {
                curr = curr->sides[1];
            }

            printf("%d  ", curr->id);
        } while (curr->sides[1] != 0);

        while (curr->sides[3] != 0) {
            curr = curr->sides[3];
        }

        printf("\n");
    } while (curr->sides[2] != 0);

    printf("\n\n");

    char *img = (char*)calloc(8 * 8 * side * side + 1, sizeof(char));
    formatImg(c0, img);

    char *p = img;
    while (p < img + strlen(img)) {
        char *temp = (char *)calloc(8 * side + 1, sizeof(char));
        strncpy(temp, p, 8 * side);
        printf("%s\n", temp);
        p += 8 * side;
    }
    writeFile(img);

    side = (test) ? 24 : 96;
    dataLine = 100;

    printf("\n\nWater Roughness: %d\n", roughness());

    return 1;
}
