#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#include "C:\Users\Brandon Hippe\Documents\Coding Projects\Advent-of-Code\Modules\input.h"
#include "C:\Users\Brandon Hippe\Documents\Coding Projects\Advent-of-Code\Modules\dict.h"
#include "C:\Users\Brandon Hippe\Documents\Coding Projects\Advent-of-Code\Modules\heapq.h"
#define fileName "input.txt"


char *pointStr(int x, int y) {
    int sizex = ceil(log10(abs(x) + 1)), sizey = ceil(log10(abs(y) + 1));
    char *str = (char*)calloc(sizex + sizey + 2, sizeof(char));
    sprintf(str, "%d,%d", x, y);
    return str;
}


int aStar(struct dict *area, char *start, char *end) {
    
}


int main () {
    struct vector *input_data = multiLine(fileName);
    struct dict *areaP1 = createDict(stringsize, intsize, copyElement);

    for (int y = 0; y < input_data->len; y++) {
        char *line = (char*)input_data->arr[y];
        for (int x = 0; x < strlen(line); x++) {
            char *spot = (char*)calloc(2, sizeof(char));
            strncpy(spot, line + x, 1);
            int *val = (int*)calloc(1, sizeof(int));
            *val = atoi(spot);

            addDict(areaP1, pointStr(x, y), val);
        }
    }

    printf("\nPart 1:\nLowest risk: %d\n", aStar(areaP1, pointStr(0, 0), pointStr(input_data->len - 1, input_data->len - 1)));

    return 1;
}
