#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#define fileName "input.txt"
#define dataLine 20
#define buffer 25

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

int findMin(int *nums, int start, int end) {
    int min = nums[start];
    for (int i = start; i < end; i++) {
        if (nums[i] < min) {
            min = nums[i];
        }
    }

    return min;
}

int findMax(int *nums, int start, int end) {
    int max = nums[start];
    for (int i = start; i < end; i++) {
        if (nums[i] > max) {
            max = nums[i];
        }
    }

    return max;
}

int main () {
    int numLines, error;
	numLines = findLines();

	if (numLines == -1) {
        printf("Error: Could not read input file. Quitting\n");
        return -1;
	}

	int nums[numLines];

    readData(&nums[0]);

    for (int i = buffer; i < numLines; i++) {
        bool valid = false;
        for (int j = i - buffer; j < i - 1; j++) {
            for (int k = j + 1; k < i; k++) {
                if (nums[j] + nums[k] == nums[i]) {
                    valid = true;
                    break;
                }
            }

            if (valid) {
                break;
            }
        }

        if (!valid) {
            error = nums[i];
            printf("Invalid found: %d\n", nums[i]);
        }
    }

    for (int i = 2; i < numLines; i++) {
        for (int j = 0; j < numLines; j++) {
            int count = 0;
            for (int k = j; (k < j + i && k < numLines); k++) {
                count += nums[k];
            }

            if (count == error) {
                printf("The following numbers sum to the error:\n");
                for (int k = j; (k < j + i && k < numLines); k++) {
                    printf("%d\n", nums[k]);
                }

                int min = findMin(&nums[0], j, j + i);
                int max = findMax(&nums[0], j, j + i);
                printf("The encryption weakness is: %d\n", min + max);
            }
        }
    }



	printf("\nProgram Done");


	return 1;
}
