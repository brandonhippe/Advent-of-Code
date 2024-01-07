#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>

int main () {
    bool test = false;
    int part = 2, end, start = (test) ? 4 : 7;

    switch (part) {
        case 1:
            end = 2020;
            break;
        case 2:
            end = 30000000;
            break;
        default:
            end = 10;
    }

    int *spoken = (int*)calloc(end + 1, sizeof(int));


    if (test) {
        spoken[0] = 1;
        spoken[3] = 2;
    } else {
        spoken[14] = 1;
        spoken[3] = 2;
        spoken[1] = 3;
        spoken[0] = 4;
        spoken[9] = 5;
    }

    int prev = (test) ? 6 : 5;

    for (int i = start; i <= end; i++) {
        int temp = prev;

        if (spoken[temp] > 0) {
            prev = i - spoken[temp] - 1;
        } else {
            prev = 0;
        }

        spoken[temp] = i - 1;
    }

    printf("The %dth number spoken was %d.\n", end, prev);

	return 1;
}
