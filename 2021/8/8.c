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


bool charcmp(void *a, void *b) {
    return *(char*)a < *(char*)b;
}


int getOutput(struct dict *pairs, char *outputStr) {
    struct vector *corrected = createVector(charsize, copyElement);

    for (int i = 0; i < strlen(outputStr); i++) {
        char *c = (char*)calloc(1, sizeof(char));
        *c = outputStr[i];
        appendVector(corrected, getDictVal(pairs, c));
    }

    char *correctedStr = getLine(sortVector(corrected, charcmp));

    if (strcmp(correctedStr, "abcefg") == 0) {
        return 0;
    } else if (strcmp(correctedStr, "cf") == 0) {
        return 1;
    } else if (strcmp(correctedStr, "acdeg") == 0) {
        return 2;
    } else if (strcmp(correctedStr, "acdfg") == 0) {
        return 3;
    } else if (strcmp(correctedStr, "bcdf") == 0) {
        return 4;
    } else if (strcmp(correctedStr, "abdfg") == 0) {
        return 5;
    } else if (strcmp(correctedStr, "abdefg") == 0) {
        return 6;
    } else if (strcmp(correctedStr, "acf") == 0) {
        return 7;
    } else if (strcmp(correctedStr, "abcdefg") == 0) {
        return 8;
    } else if (strcmp(correctedStr, "abcdfg") == 0) {
        return 9;
    }

    return -1;
}


int main () {
    struct vector *input_data = multiLine(fileName);
    struct dict *occurrances = createDict(intsize, stringsize, copyElement);
    
    for (int i = (int)'a'; i <= (int)'g'; i++) {
        char *c = (char*)calloc(2, sizeof(char));
        int *occ = (int*)calloc(1, sizeof(int));

        *c = (char)i;
        switch (i) {
            case 'a':
                *occ = 344;
                break;
            case 'b':
                *occ = 204;
                break;
            case 'c':
                *occ = 304;
                break;
            case 'd':
                *occ = 266;
                break;
            case 'e':
                *occ = 96;
                break;
            case 'f':
                *occ = 396;
                break;
            case 'g':
                *occ = 280;
                break;
        }

        addDict(occurrances, occ, c);
    }

    int outputSum = 0, easyCount = 0;
    for (int i = 0; i < input_data->len; i++) {
        char *str = (char*)input_data->arr[i], *pattern = strtok(str, "|"), *output = strtok(NULL, "|");
        struct dict *totalLen = createDict(charsize, intsize, copyElement), *frequency = createDict(charsize, intsize, copyElement);
        
        char *p = strtok(pattern, " ");
        while (p) {
            for (int j = 0; j < strlen(p); j++) {
                char *c = (char*)calloc(1, sizeof(char));
                *c = p[j];
                if (!inDict(totalLen, c)) {
                    addDict(totalLen, c, calloc(1, sizeof(int)));
                    addDict(frequency, c, calloc(1, sizeof(int)));
                }

                int *l = getDictVal(totalLen, c), *f = getDictVal(frequency, c);
                *l = *l + strlen(p);
                *f = *f + 1;
            }

            p = strtok(NULL, " ");
        }

        struct vector *chars = keys2vector(totalLen), *lens = values2vector(totalLen);
        struct dict *pairs = createDict(charsize, charsize, copyElement);
        for (int i = 0; i < chars->len; i++) {
            char *c = (char*)chars->arr[i];
            int *lenFreq = (int*)lens->arr[i];
            *lenFreq *= *(int*)getDictVal(frequency, c);
            addDict(pairs, c, getDictVal(occurrances, lenFreq));
        }

        int outputNum = 0;
        p = strtok(output, " ");
        while (p) {
            int o = getOutput(pairs, p);
            if (o == 1 || o == 4 || o == 7 || o  == 8) {
                easyCount++;
            }

            outputNum *= 10;
            outputNum += o;

            p = strtok(NULL, " ");
        }

        outputSum += outputNum;
    }

    printf("\nPart 1:\nOccurances of 1, 4, 7, and 8: %d\n\nPart 2:\nSum of Output Values: %d\n", easyCount, outputSum);

    return 1;
}
