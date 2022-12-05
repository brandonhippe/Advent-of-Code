#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#include "C:\Users\Brandon Hippe\Documents\Coding Projects\Advent-of-Code\Modules\input.h"
#define fileName "input.txt"


bool ullcmp(void *e1, void *e2) {
    return *(unsigned long long *)e1 <= *(unsigned long long *)e2;
}


int main () {
    struct vector *input_data = multiLine(fileName), *scores = createVector(ullsize, copyElement);
    int corruptedScore = 0;

    for (int i = 0; i < input_data->len; i++) {
        char *line = (char*)input_data->arr[i];

        struct vector *stack = createVector(charsize, copyElement);

        int j;
        for (j = 0; j < strlen(line); j++) {
            char *c;
            if (line[j] == '(' || line[j] == '[' || line[j] == '{' || line[j] == '<') {
                c = (char*)calloc(1, sizeof(char));
                *c = line[j];
                appendVector(stack, c);
            } else {
                c = popVector(stack);
                if (!((*c == '(' && line[j] == ')') || (*c == '[' && line[j] == ']') || (*c == '{' && line[j] == '}') || (*c == '<' && line[j] == '>'))) {
                    break;
                }
            }
        }

        if (j != strlen(line)) {
            switch (line[j]) {
                case ')':
                    corruptedScore += 3;
                    break;
                case ']':
                    corruptedScore += 57;
                    break;
                case '}':
                    corruptedScore += 1197;
                    break;
                case '>':
                    corruptedScore += 25137;
                    break;
            }

            continue;
        }

        unsigned long long *score = (unsigned long long *)calloc(1, sizeof(unsigned long long));
        while (stack->len != 0) {
            char *c = (char*)popVector(stack);
            *score *= 5;
            switch (*c) {
                case '(':
                    *score += 1;
                    break;
                case '[':
                    *score += 2;
                    break;
                case '{':
                    *score += 3;
                    break;
                case '<':
                    *score += 4;
                    break;
            }
        }

        appendVector(scores, score);
    }

    scores = sortVector(scores, ullcmp);

    printf("\nPart 1:\nTotal Syntax Error for Corrupted Lines: %d\n\nPart 2:\nMiddle Incomplete Score: %llu\n", corruptedScore, *(unsigned long long *)scores->arr[scores->len / 2]);

    return 1;
}