#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#include "C:\Users\Brandon Hippe\Documents\Coding Projects\Advent-of-Code\Modules\input.h"
#define fileName "input.txt"


size_t ullsize(void *e) {
    return sizeof(unsigned long long);
}


unsigned long long countFish(struct vector *fish) {
    unsigned long long count = 0;
    for (int i = 0; i < fish->len; i++) {
        count += *(unsigned long long*)fish->arr[i];
    }

    return count;
}


int main () {
    struct vector *input_data = singleLine(fileName, ",");
    struct vector *fish = createVector(ullsize, copyElement);

    for (int i = 0; i < 9; i++) {
        unsigned long long *n = (unsigned long long*)calloc(1, sizeof(int));
        *n = 0;
        appendVector(fish, n);
    }

    for (int i = 0; i < input_data->len; i++) {
        *(unsigned long long*)(fish->arr[atoi(input_data->arr[i])]) = *(unsigned long long*)(fish->arr[atoi(input_data->arr[i])]) + 1;
    }

    for (int i = 0; i < 256; i++) {
        if (i == 80) {
            printf("\nPart 1:\nNumber of fish after 80 days: %llu\n", countFish(fish));
        }

        unsigned long long *reproduced = (unsigned long long*)fish->arr[0];
        fish = sliceVector(fish, 1, fish->len, 1);
        *(unsigned long long*)fish->arr[6] += *reproduced;
        appendVector(fish, reproduced);
    }

    printf("\nPart 2:\nNumber of fish after 256 days: %llu\n", countFish(fish));

    return 1;
}
