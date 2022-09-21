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
        dataLine[i] = *((char*)line->arr[i]);
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
            deleteVector(line, false);
            line = createVector(charsize, copyElement);
        } else if (*c != -1) {
            appendVector(line, c);
        }
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
    struct vector *data = createVector(stringsize, copyElement);

    FILE *fp = fopen(fileName, "r");
    if (!fp) {
        return NULL;
    }

    struct vector *line = createVector(charsize, copyElement);

    while (!feof(fp)) {
        char *c = (char*)calloc(2, sizeof(char));
        *c = fgetc(fp);
        if (*c != -1) {
            appendVector(line, c);
        }
    }

    char *input_line = getLine(line);
    deleteVector(line, false);

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