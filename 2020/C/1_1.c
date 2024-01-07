#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#define fileName "input.txt"
#define dataLine 20

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

void readData(int *nums) {
    int lineNum = 0;
	char textRead[dataLine];

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return;
    }

	while(fgets(textRead, dataLine, inFile)) {
        nums[lineNum] = atoi(textRead);

        lineNum++;
	}

	fclose(inFile);

    return;
}

int main () {
    int numLines, product;
	numLines = findLines();

	if (numLines == -1) {
        printf("Error: Could not read input file. Quitting\n");
        return -1;
	}

	int nums[numLines];

    readData(&nums[0]);

    for (int i = 0; i < numLines - 1; i++) {
        for (int j = i + 1; j < numLines; j++) {
            if (nums[i] + nums[j] == 2020) {
                product = nums[i] * nums[j];
            }
        }
    }

    printf("Product of numbers that sum to 2020: %d\n", product);

	printf("\nProgram Done");

	return 1;
}
