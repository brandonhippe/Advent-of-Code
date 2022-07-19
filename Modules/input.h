#ifndef INPUT_H
#define INPUT_H


#include <stdlib.h>
#include <stdio.h>
#include "vector.h"


struct vector *readInput(char *fileName);


void appendLine(struct vector *data, struct vector *line) {
    int len = line->len;
    char *dataLine = (char*)calloc(len + 1, sizeof(char));

    for (int i = 0; i < len; i++) {
        char c = *(char*)pop(line, 0);
        if (c != -1) {
            dataLine[i] = c;
        }
    }
    
    append(data, dataLine);
}


struct vector *readInput(char *fileName) {
    struct vector *data = createVector();

    FILE *fp = fopen(fileName, "r");
    if (!fp) {
        return NULL;
    }

    struct vector *line = createVector();

    while (!feof(fp)) {
        char *c = (char*)calloc(2, sizeof(char));
        *c = fgetc(fp);

        if (*c == '\n') {
            appendLine(data, line);
        } else {
            append(line, c);
        }
    }

    if (line->len != 0) {
        appendLine(data, line);
    }

    deleteVector(line);

    return data;
}


#endif