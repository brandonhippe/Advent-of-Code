#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#include "../../Modules/input.h"
#include "../../Modules/set.h"
#define fileName "../../Inputs/2021_13.txt"


char *pointStr(int x, int y) {
    int sizex = ceil(log10(abs(x) + 1)), sizey = ceil(log10(abs(y) + 1));
    char *str = (char*)calloc(sizex + sizey + 2, sizeof(char));
    sprintf(str, "%d,%d", x, y);
    return str;
}


int main () {
    struct vector *input_data = multiLine(fileName);

    struct set *points = createSet(stringsize, copyElement);
    int i = 0;
    for (i = 0; i < input_data->len; i++) {
        char *line = (char*)input_data->arr[i];
        if (strlen(line) == 0) {
            break;
        }

        addSet(points, line);
    }

    i++;

    int minx, maxx, miny, maxy;
    for (int j = 0; j + i < input_data->len; j++) {
        struct set *newPoints = createSet(stringsize, copyElement);
        char *instruction = (char*)copyElement(input_data->arr[i + j], stringsize(input_data->arr[i + j])), *p = strtok(instruction, "=");
        char dir = p[strlen(p) - 1];
        p = strtok(NULL, "=");
        int fold = atoi(p);

        struct vector *folding = set2vector(points);
        for (int k = 0; k < folding->len; k++) {
            char *point = (char*)copyElement(folding->arr[k], stringsize(folding->arr[k]));
            int x, y;

            p = strtok(point, ",");
            x = atoi(p);
            p = strtok(NULL, ",");
            y = atoi(p);

            if (dir == 'x') {
                if (x > fold) {
                    x = fold - (x - fold);
                }
            } else {
                if (y > fold) {
                    y = fold - (y - fold);
                }
            }

            if (k == 0) {
                minx = x;
                maxx = x;
                miny = y;
                maxy = y;
            } else {
                if (x < minx) {
                    minx = x;
                }

                if (x > maxx) {
                    maxx = x;
                }

                if (y < miny) {
                    miny = y;
                }

                if (y > maxy) {
                    maxy = y;
                }
            }

            addSet(newPoints, pointStr(x, y));
        }

        deleteSet(points, true);
        points = newPoints;

        if (j == 0) {
            printf("\nPart 1:\nNumber of dots after first fold: %d\n", points->len);
        }
    }

    printf("\nPart 2:\n");
    for (int y = miny; y <= maxy; y++) {
        for (int x = minx; x <= maxx; x++) {
            printf("%c", (inSet(points, pointStr(x, y))) ? '#' : ' ');
        }
        
        printf("\n");
    }

    return 1;
}
