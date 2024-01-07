#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#include "C:\Users\Brandon Hippe\Documents\Coding Projects\Advent-of-Code\Modules\input.h"
#include "C:\Users\Brandon Hippe\Documents\Coding Projects\Advent-of-Code\Modules\dict.h"
#define fileName "input.txt"


int maxVal(struct dict *d) {
    struct vector *vals = values2vector(d);
    int max = *(int*)vals->arr[0];
    for (int i = 1; i < vals->len; i++) {
        if (*(int*)vals->arr[i] > max) {
            max = *(int*)vals->arr[i];
        }
    }

    return max;
}


int findPaths(struct dict *neighborData, struct dict *visitedData, char *node, bool p2) {
    if (strcmp(node, "end") == 0) {
        return 1;
    }

    if (!inDict(visitedData, node)) {
        int *times = (int*)calloc(1, sizeof(int));
        addDict(visitedData, node, times);
    }

    int *nodeVisitTimes = (int*)getDictVal(visitedData, node), paths = 0;
    if (node[0] == tolower(node[0])) {
        *nodeVisitTimes = *nodeVisitTimes + 1;
    }

    struct vector *neighbors = (struct vector *)getDictVal(neighborData, node);
    for (int i = 0; i < neighbors->len; i++) {
        char *n = (char*)neighbors->arr[i];
        if (strcmp(n, "start") == 0) {
            continue;
        }

        if (!inDict(visitedData, n)) {
            int *times = (int*)calloc(1, sizeof(int));
            addDict(visitedData, n, times);
        }

        if (*(int*)getDictVal(visitedData, n) == 0 || (p2 && maxVal(visitedData) == 1)) {
            paths += findPaths(neighborData, visitedData, n, p2);
        }
    }

    if (node[0] == tolower(node[0])) {
        *nodeVisitTimes = *nodeVisitTimes - 1;
    }

    return paths;
}


int main () {
    struct vector *input_data = multiLine(fileName);
    struct dict *neighborData = createDict(stringsize, sizeofVector, createCopyVector), *visitedData = createDict(stringsize, intsize, copyElement);

    for (int i = 0; i < input_data->len; i++) {
        char *line = (char*)calloc(strlen((char*)input_data->arr[i]), sizeof(char));
        strcpy(line, input_data->arr[i]);

        char *p1 = strtok(line, "-"), *p2 = strtok(NULL, "-");
        
        if (!inDict(neighborData, p1)) {
            struct vector *nVec = createVector(stringsize, copyElement);
            addDict(neighborData, p1, nVec);
        }

        if (!inDict(neighborData, p2)) {
            struct vector *nVec = createVector(stringsize, copyElement);
            addDict(neighborData, p2, nVec);
        }
        
        struct vector *p1Vec = (struct vector *)getDictVal(neighborData, p1), *p2Vec = (struct vector *)getDictVal(neighborData, p2);
        
        appendVector(p1Vec, p2);
        appendVector(p2Vec, p1);
    }

    printf("\nPart 1:\nNumber of paths visiting small caves at most once: %d\n\nPart 2:\nNumber of paths visiting small caves at most twice: %d\n", findPaths(neighborData, visitedData, "start", false), findPaths(neighborData, visitedData, "start", true));

    return 1;
}
