#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include "C:\Users\Brandon Hippe\Documents\Coding Projects\Advent-of-Code\Modules\input.h"
#include "C:\Users\Brandon Hippe\Documents\Coding Projects\Advent-of-Code\Modules\vector.h"
#define fileName "input.txt"


int main () {
    struct vector *input_data = multiLine(fileName);
    struct vector *data = createVector(intsize, copyElement);

    for (int i = 0; i < input_data->len; i++) {
        int *d = (int*)calloc(1, sizeof(1));
        char *str = input_data->arr[i];
        for (int j = 0; j < strlen(str); j++) {
            *d *= 2;
            *d += (str[j] == '1') ? 1 : 0;
        }

        appendVector(data, d);
    }

    int gamma = 0, epsilon = 0, mask = 0b100000000000;
    while (mask > 0) {
        int zcount = 0, ocount = 0;
        for (int i = 0; i < data->len; i++) {
            int *n = data->arr[i];

            if (*n & mask) {
                ocount += 1;
            } else {
                zcount += 1;
            }
        }

        gamma *= 2;
        gamma += (ocount > zcount) ? 1 : 0;

        epsilon *= 2;
        epsilon += (ocount > zcount) ? 0 : 1;

        mask /= 2;
    }

    printf("\nPart 1:\nGamma (%d) * Epsilon (%d) = %d\n", gamma, epsilon, gamma * epsilon);

    struct vector *mostCommon = createCopyVector(data, sizeof(struct vector));
    struct vector *leastCommon = createCopyVector(data, sizeof(struct vector));

    mask = 0b100000000000;

    while (mask > 0) {
        if (mostCommon->len > 1) {
            struct vector *oneset = createVector(intsize, copyElement);
            struct vector *zeroset = createVector(intsize, copyElement);
        
            for (int i = 0; i < mostCommon->len; i++) {
                if (*(int*)mostCommon->arr[i] & mask) {
                    appendVector(oneset, mostCommon->arr[i]);
                } else {
                    appendVector(zeroset, mostCommon->arr[i]);
                }
            }

            deleteVector(mostCommon);
            if (oneset->len >= zeroset->len) {
                deleteVector(zeroset);
                mostCommon = oneset;
            } else {
                deleteVector(oneset);
                mostCommon = zeroset;
            }
        }

        if (leastCommon->len > 1) {
            struct vector *oneset = createVector(intsize, copyElement);
            struct vector *zeroset = createVector(intsize, copyElement);
            
            for (int i = 0; i < leastCommon->len; i++) {
                if (*(int*)leastCommon->arr[i] & mask) {
                    appendVector(oneset, leastCommon->arr[i]);
                } else {
                    appendVector(zeroset, leastCommon->arr[i]);
                }
            }

            deleteVector(leastCommon);
            if (zeroset->len <= oneset->len) {
                deleteVector(oneset);
                leastCommon = zeroset;
            } else {
                deleteVector(zeroset);
                leastCommon = oneset;
            }
        }

        mask /= 2;
    }

    int o2 = *(int*)mostCommon->arr[0], co2 = *(int*)leastCommon->arr[0];
    printf("\nPart 2:\nO2 Rating (%d) * CO2 Rating (%d) = %d\n", o2, co2, o2 * co2);

    return 1;
}
