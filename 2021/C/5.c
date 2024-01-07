#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#include "C:\Users\Brandon Hippe\Documents\Coding Projects\Advent-of-Code\Modules\input.h"
#include "C:\Users\Brandon Hippe\Documents\Coding Projects\Advent-of-Code\Modules\set.h"
 #define fileName "input.txt"


char *pointStr(int x, int y) {
    int sizex = ceil(log10(x + 1)), sizey = ceil(log10(y + 1));
    char *str = (char*)calloc(sizex + sizey + 2, sizeof(char));
    sprintf(str, "%d,%d", x, y);
    return str;
}


int *placePoints(struct vector *lines) {
    struct set *points = createSet(stringsize, copyElement), *intersections = createSet(stringsize, copyElement);
    struct set *hvpoints = createSet(stringsize, copyElement), *hvintersections = createSet(stringsize, copyElement);

    for (int i = 0; i < lines->len; i++) {
        printf("%d/%d\r", i + 1, lines->len);
        struct vector *line = (struct vector *)lines->arr[i];
        int x = *(int*)line->arr[0], y = *(int*)line->arr[1], xend = *(int*)line->arr[2], yend = *(int*)line->arr[3], xdiff = *(int*)line->arr[4], ydiff = *(int*)line->arr[5];
        bool hv = xdiff == 0 || ydiff == 0;

        while (x != xend || y != yend) {
            char *pos = pointStr(x, y);
            if (inSet(points, pos)) {
                addSet(intersections, pos);
                removeSet(points, pos);
            } else if (!inSet(intersections, pos)) {
                addSet(points, pos);
            }

            if (hv) {
                if (inSet(hvpoints, pos)) {
                    addSet(hvintersections, pos);
                    removeSet(hvpoints, pos);
                } else if (!inSet(hvintersections, pos)) {
                    addSet(hvpoints, pos);
                }
            }

            x += xdiff;
            y += ydiff;
        } 

        char *pos = pointStr(x, y);
        if (inSet(points, pos)) {
            addSet(intersections, pos);
        } else {
            addSet(points, pos);
        }

        if (hv) {
            if (inSet(hvpoints, pos)) {
                addSet(hvintersections, pos);
                removeSet(hvpoints, pos);
            } else if (!inSet(hvintersections, pos)) {
                addSet(hvpoints, pos);
            }
        }
    }

    printf("\n");

    int *intPoints = (int*)calloc(2, sizeof(int));
    intPoints[0] = hvintersections->len;
    intPoints[1] = intersections->len;

    deleteSet(points, true);
    deleteSet(intersections, true);
    deleteSet(hvpoints, true);
    deleteSet(hvintersections, true);

    return intPoints;
}


int main () {
    struct vector *input_data = multiLine(fileName), *all = createVector(sizeofVector, createCopyVector);

    for (int i = 0; i < input_data->len; i++) {
        char *str = (char*)input_data->arr[i], *p;
        int size = 0, start = -1, ix = 0;
        struct vector *line = createVector(intsize, copyElement);

        for (int j = 0; j < strlen(str); j++) {
            if (isdigit(str[j]) != 0) {
                if (start == -1) {
                    start = j;
                }

                size += 1;
            } else if (start >= 0) {
                p = (char*)calloc(size, sizeof(char));
                strncpy(p, str + start, size);
                int *n = (int*)calloc(1, sizeof(int));
                *n = atoi(p);
                appendVector(line, n);
                size = 0;
                ix++;
                start = -1;
                free(p);
            }
        }

        p = (char*)calloc(size, sizeof(char));
        strncpy(p, str + start, size);
        int *n = (int*)calloc(1, sizeof(int));
        *n = atoi(p);
        appendVector(line, n);
        free(p);

        int *xinc = (int*)calloc(1, sizeof(int)), *yinc = (int*)calloc(1, sizeof(int));
        *xinc = (*(int*)line->arr[0] == *(int*)line->arr[2]) ? 0 : ((*(int*)line->arr[0] < *(int*)line->arr[2]) ? 1 : -1);
        *yinc = (*(int*)line->arr[1] == *(int*)line->arr[3]) ? 0 : ((*(int*)line->arr[1] < *(int*)line->arr[3]) ? 1 : -1);
        appendVector(line, xinc);
        appendVector(line, yinc);
        free(input_data->arr[i]);

        appendVector(all, line);
    }

    void *temp = all->arr[463];
    all->arr[463] = all->arr[0];
    all->arr[0] = temp;

    int *intPoints = placePoints(all);

    printf("\nPart 1:\nDangerous Points: %d\n\nPart 2:\nDangerous Points: %d\n", intPoints[0], intPoints[1]);

    return 1;
}
