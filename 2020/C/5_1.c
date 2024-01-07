#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#define fileName "input.txt"
#define dataLine 15

int findLines() {
	int numLines = 0;
	char textRead[dataLine];

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        ++numLines;
	}

	fclose(inFile);

	return numLines;
}

void readData(int *seats) {
    int index = 0;
	char textRead[dataLine], *p;

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        p = strtok(textRead, "\n");
        for (int i = 0; i < 10; i++) {
            if (p[i] == 'F' || p[i] == 'L') {
                p[i] = '0';
            } else if (p[i] == 'B' || p[i] == 'R') {
                p[i] = '1';
            }
        }

        int num = strtol(p, NULL, 2);
        seats[index] = num;
        index++;
	}

	fclose(inFile);

    return;
}

int findMax(int *arr, int total) {
    int max = 0;
    for (int i = 0; i < total; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }

    return max;
}

int main () {
	int numLines, count = 0, max;

	numLines = findLines();

	if (numLines == -1) {
        printf("Error: Could not read input file. Quitting\n");
        return -1;
	}

    int seats[numLines];

    readData(&seats[0]);

    max = findMax(&seats[0], numLines);

    printf("Max: %d\n", max);

	printf("\nProgram Done");


	return 1;
}

