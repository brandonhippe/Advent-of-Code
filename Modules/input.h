#ifndef INPUT_H
#define INPUT_H


// Include header files
#include <stdlib.h>
#include <stdio.h>
#include "vector.h"


// Function Prototypes
struct vector *multiLine(char *fileName);
struct vector *singleLine(char *fileName, char *delim);


// Function to convert single dataline vector to a string
char *getLine(struct vector *line) {
    int len = line->len;
    char *dataLine = (char*)calloc(len + 2, sizeof(char));

    for (int i = 0; i < len; i++) {
        memcpy(dataLine + i, line->arr[i], sizeof(char));
    }
    
    return dataLine;
}


// Function to read multi-line input from a file
struct vector *multiLine(char *fileName) {
    struct vector *data = createVector(stringsize, copyElement);

    FILE *fp = fopen(fileName, "r");
    if (!fp) {
        return NULL;
    }

    struct vector *line = createVector(charsize, copyElement);

    while (!feof(fp)) {
        char *c = (char*)calloc(1, sizeof(char));
        *c = fgetc(fp);

        if (*c == '\n') {
            char *l = getLine(line);
            appendVector(data, l);
            deleteVector(line, true);
            line = createVector(charsize, copyElement);
        } else if (*c != -1) {
            appendVector(line, c);
        }

        free(c);
    }

    if (line->len != 0) {
        char *l = getLine(line);
        appendVector(data, l);
    }

    deleteVector(line, false);

    return data;
}


// Function to read single line input from a file, separated by delim
struct vector *singleLine(char *fileName, char *delim) {
    FILE *fp = fopen(fileName, "r");
    if (!fp) {
        return NULL;
    }

    char *input_line = (char*)calloc(2, sizeof(char));
    int ix = 0, max_chars = 1;

    while (!feof(fp)) {
        char c = fgetc(fp);

        if (c != -1) {
            if (ix == max_chars) {
                input_line = (char*)realloc(input_line, (2 * max_chars + 1) * sizeof(char));
                max_chars *= 2;
            }

            input_line[ix] = c;
            ix++;
        }
    }

    struct vector *data = createVector(stringsize, copyElement);

    char *p = strtok(input_line, delim);
    while (p) {
        char *e = (char*)calloc(strlen(p), sizeof(char));
        strcpy(e, p);
        appendVector(data, e);
        p = strtok(NULL, delim);
    }

    return data;
}


#endif