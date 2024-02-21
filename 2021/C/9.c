#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#include "../../Modules/input.h"
#include "../../Modules/dict.h"
#include "../../Modules/set.h"
#define fileName "../../Inputs/2021_9.txt"


char *pointStr(int x, int y) {
    int sizex = ceil(log10(abs(x) + 1)), sizey = ceil(log10(abs(y) + 1));
    char *str = (char*)calloc(sizex + sizey + 2, sizeof(char));
    sprintf(str, "%d,%d", x, y);
    return str;
}


struct vector *strPoint(char *pStr) {
    struct vector *point = createVector(intsize, copyElement);
    char *p = strtok(pStr, ",");
    while (p) {
        int *n = (int*)calloc(1, sizeof(int));
        *n = atoi(p);
        appendVector(point, n);

        p = strtok(NULL, ",");
    }

    return point;
}


int basinSize(char *lowPos, struct set *visited, struct dict *area) {
    addSet(visited, lowPos);

    char *lowPosCopy = (char*)calloc(strlen(lowPos), sizeof(char));
    strcpy(lowPosCopy, lowPos);

    struct vector *pos = strPoint(lowPosCopy);
    int x = *(int*)pos->arr[0], y = *(int*)pos->arr[1], size = 0;

    for (int j = -1; j <= 1; j += 2) {
        if (inDict(area, pointStr(x + j, y)) && *(int*)getDictVal(area, pointStr(x + j, y)) != 9 && !inSet(visited, pointStr(x + j, y))) {
            size += 1 + basinSize(pointStr(x + j, y), visited, area);
        }

        if (inDict(area, pointStr(x, y + j)) && *(int*)getDictVal(area, pointStr(x, y + j)) != 9 && !inSet(visited, pointStr(x, y + j))) {
            size += 1 + basinSize(pointStr(x, y + j), visited, area);
        }
    }

    return size;
}


bool intcmp(void *e1, void *e2) {
    return *(int*)e1 <= *(int*)e2;
}


int main () {
    struct vector *input_data = multiLine(fileName);
    struct dict *area = createDict(stringsize, intsize, copyElement);

    for (int i = 0; i < input_data->len; i++) {
        char *l = (char*)input_data->arr[i];
        for (int j = 0; j < strlen(l); j++) {
            int *n = (int*)calloc(1, sizeof(int));
            char *p = (char*)calloc(1, sizeof(char));
            strncpy(p, &l[j], 1);
            *n = atoi(p);
            addDict(area, pointStr(j, i), n);
        }
    }

    struct vector *points = keys2vector(area);
    struct set *lowPoints = createSet(stringsize, copyElement);
    int risk = 0;

    for (int i = 0; i < points->len; i++) {
        char *posStr = (char*)calloc(strlen((char*)points->arr[i]), sizeof(char));
        strcpy(posStr, (char*)points->arr[i]);
        struct vector *point = strPoint(posStr);
        int x = *(int*)point->arr[0], y = *(int*)point->arr[1], val = *(int*)getDictVal(area, points->arr[i]);

        bool lowest = true;
        for (int j = -1; j <= 1; j += 2) {
            if (inDict(area, pointStr(x, y + j)) && *(int*)getDictVal(area, pointStr(x, y + j)) <= val) {
                lowest = false;
                break;
            }

            if (inDict(area, pointStr(x + j, y)) && *(int*)getDictVal(area, pointStr(x + j, y)) <= val) {
                lowest = false;
                break;
            }
        }

        if (lowest) {
            addSet(lowPoints, points->arr[i]);
            risk += val + 1;
        }
    }

    printf("\nPart 1:\nRisk level of all low points: %d\n", risk);

    struct vector *lowP = set2vector(lowPoints), *basins = createVector(intsize, copyElement);
    for (int i = 0; i < lowP->len; i++) {
        int *bSize = (int*)calloc(1, sizeof(int));
        *bSize = basinSize((char*)lowP->arr[i], createSet(stringsize, copyElement), area);
        appendVector(basins, bSize);
    }

    basins = sortVector(basins, intcmp);
    printf("\nPart 2:\nProduct of 3 largest basins: %d * %d * %d = %d\n", *(int*)basins->arr[basins->len - 1], *(int*)basins->arr[basins->len - 2], *(int*)basins->arr[basins->len - 3], *(int*)basins->arr[basins->len - 1] * *(int*)basins->arr[basins->len - 2] * *(int*)basins->arr[basins->len - 3]);

    return 1;
}
