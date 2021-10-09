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

void quickSort(int *sortArray, int start, int end) {
	int pivotIndex;

	// Stop recursively calling quickSort
	if (start >= end) {
		return;
	}

	// Selects a pivot value, puts all values less than pivot value on left of pivot, all values larger than pivot on right of pivot, returns where the pivot ended up
	findPivotIndex(sortArray, start, end, &pivotIndex);

	// Sort all items before pivot index, then all items after pivot index
	quickSort(sortArray, start, pivotIndex - 1);
	quickSort(sortArray, pivotIndex + 1, end);
}

void findPivotIndex(int *sortArray, int start, int end, int *pivotIndex) {
	// Set pivot index to the start of the array
	*pivotIndex = start;

    // Set pivot value to value at end of array
    int pivotValue;
    pivotValue = sortArray[end];

    // Check each item to see if it is less than the pivot value. Swap and increment pivot index if less
    for (int i = start; i < end; ++i) {
        if (sortArray[i] < pivotValue) {
            swap(sortArray, i, *pivotIndex);
            ++*pivotIndex;
        }
    }

    // Swap the pivot value and the current item at pivot index
    swap(sortArray, *pivotIndex, end);
}

void swap (int *array, int a, int b) {
	int temp;

	// Only swap if indecies are different
    if (a != b) {
        temp = array[a];
        array[a] = array[b];
        array[b] = temp;
    }
}

int main () {
    int numLines, error;
	numLines = findLines();

	if (numLines == -1) {
        printf("Error: Could not read input file. Quitting\n");
        return -1;
	}

	int nums[numLines + 2];

    readData(&nums[0]);
    nums[numLines] = 0;

    quickSort(&nums[0], 0, numLines);

    nums[numLines + 1] = nums[numLines] + 3;

    int diff1 = 0, diff3 = 0;
    for (int i = 0; i <= numLines; i++) {
        if (nums[i + 1] - nums[i] == 1) {
            diff1++;
        } else if (nums[i + 1] - nums[i] == 3) {
            diff3++;
        }
    }

    printf("Difference of 1: %d\nDifference of 3: %d\nProduct: %d\n", diff1, diff3, diff1 * diff3);

	printf("\nProgram Done");

	return 1;
}
