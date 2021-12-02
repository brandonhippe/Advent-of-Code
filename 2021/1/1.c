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

void readData(int nums[]) {
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
    int numLines;
	numLines = findLines();

	if (numLines == -1) {
        printf("Error: Could not read input file. Quitting\n");
        return -1;
	}

    int nums[numLines];
    readData(nums);

    int count = 0;
    for (int i = 0; i < numLines - 1; i++) {
        count += (nums[i] < nums[i + 1]) ? 1 : 0;
    }

    printf("Part 1:\n# of increases: %d\n", count);

    count = 0;
    int frame1[3], frame2[3];
    for (int i = 0; i < numLines - 3; i++) {
        memcpy(&frame1[0], &nums[i], 3 * sizeof(int));
        memcpy(&frame2[0], &nums[i + 1], 3 * sizeof(int));

        int sums[2] = {0, 0};
        for (int j = 0; j < 3; j++) {
            sums[0] += frame1[j];
            sums[1] += frame2[j];
        }

        count += (sums[0] < sums[1]) ? 1 : 0;
    }

    printf("Part 2:\n# of increases: %d\n", count);

	printf("\nProgram Done");

	return 1;
}
