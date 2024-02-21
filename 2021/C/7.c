#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#include "../../Modules/input.h"
#define fileName "../../Inputs/2021_7.txt"


bool compareInt(void *e1, void *e2) {
    return *(int*)e1 <= *(int*)e2;
}


int triangle(int n) {
    return n * (n + 1) / 2;
}


int main () {
    struct vector *input_data = singleLine(fileName, ",");

    for (int i = 0; i < input_data->len; i++) {
        int *e = (int*)calloc(1, sizeof(int));
        *e = atoi((char*)input_data->arr[i]);
        input_data->arr[i] = e;
    }

    input_data->e_size = intsize;
    input_data = sortVector(input_data, compareInt);

    int minFuelP1 = -1, minFuelP2 = -1;

    for (int pos = *(int*)input_data->arr[0]; pos <= *(int*)input_data->arr[input_data->len - 1]; pos++) {
        int fuelP1 = 0, fuelP2 = 0;
        for (int i = 0; i < input_data->len; i++) {
            int dist = abs(pos - *(int*)input_data->arr[i]);
            fuelP1 += dist;
            fuelP2 += triangle(dist);
        }

        if (minFuelP1 == -1 || fuelP1 < minFuelP1) {
            minFuelP1 = fuelP1;
        }

        if (minFuelP2 == -1 || fuelP2 < minFuelP2) {
            minFuelP2 = fuelP2;
        }
    }

    printf("\nPart 1:\nMinimum fuel: %d\n\nPart 2:\nMinimum Fuel: %d\n", minFuelP1, minFuelP2);

    return 1;
}
