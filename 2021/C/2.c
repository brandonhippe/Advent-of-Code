#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include "../../Modules/input.h"
#include "../../Modules/vector.h"
#define fileName "../../Inputs/2021_2.txt"


struct dataline {
    int amt;
    char *str;
};

int main () {
    struct vector *input_data = multiLine(fileName);
    struct vector *data = createVector(stringsize, copyElement);

    for (int i = 0; i < input_data->len; i++) {
        struct dataline *dline = (struct dataline*)calloc(1, sizeof(struct dataline));
        char *line = (char*)input_data->arr[i];
        char *p = strtok(line, " ");
        dline->str = (char*)calloc(strlen(p), sizeof(char));
        strcpy(dline->str, p);
        p = strtok(NULL, " ");
        dline->amt = atoi(p);
        appendVector(data, dline);
    }

    int x = 0, y = 0;
    for (int i = 0; i < data->len; i++) {
        struct dataline *dline = (struct dataline*)data->arr[i];
        if (strcmp(dline->str, "forward") == 0) {
            x += dline->amt;
        } else {
            y += (strcmp(dline->str, "up") == 0) ? -dline->amt : dline->amt;
        }
    }

    printf("\nPart 1:\nFinal pos: (%d, %d)\nAnswer: %d\n", x, y, x * y);


    int aim = 0;
    x = 0;
    y = 0;
    for (int i = 0; i < data->len; i++) {
        struct dataline *dline = (struct dataline*)data->arr[i];
        if (strcmp(dline->str, "forward") == 0) {
            x += dline->amt;
            y += aim * dline->amt;
        } else {
            aim += (strcmp(dline->str, "up") == 0) ? -dline->amt : dline->amt;
        }
    }

    printf("\nPart 2:\nFinal pos: (%d, %d)\nAnswer: %d\n", x, y, x * y);


    return 1;
}
