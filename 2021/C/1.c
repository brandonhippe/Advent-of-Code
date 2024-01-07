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
        int *val = (int*)calloc(1, sizeof(int));
        *(val) = atoi((char*)input_data->arr[i]);
        appendVector(data, val);
    }

    int increase_count = 0;
    for (int i = 1; i < data->len; i++) {
        increase_count += (*(int*)data->arr[i] > *(int*)data->arr[i - 1]) ? 1 : 0;
    }

    printf("\nPart 1:\nNumber of measurements larger than the previous element: %d\n", increase_count);
    

    struct vector *sum1 = sliceVector(data, 0, data->len - 2, 1);
    struct vector *sum2 = sliceVector(data, 1, data->len - 1, 1);
    struct vector *sum3 = sliceVector(data, 2, data->len, 1);
    
    increase_count = 0;
    for (int i = 1; i < sum1->len; i++) {
        int val = *(int*)sum1->arr[i] + *(int*)sum2->arr[i] + *(int*)sum3->arr[i];
        int pval = *(int*)sum1->arr[i - 1] + *(int*)sum2->arr[i - 1] + *(int*)sum3->arr[i - 1];
        increase_count += (val > pval) ? 1 : 0;
    }

    printf("\nPart 2:\nNumber of windows larger than previous window: %d\n", increase_count);
    

    return 1;
}
