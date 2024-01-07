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

long long findArrangements(int *arr, int start, int end) {
    if (start >= end) {
        return 1;
    }

    int i = start + 1;
    long long count = 0;

    while (arr[i] - arr[start] <= 3 && i <= end) {
        count += findArrangements(arr, i, end);
        i++;
    }

    return count;
}

int main () {
    int numLines, numReq = 1;
    long long count = 1;
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

    for (int i = 1; i < numLines + 1; i++) {
        if (nums[i + 1] - nums[i - 1] >= 4) {
            numReq++;
        }
    }

    int mustVisit[numReq], index = 1;
    mustVisit[0] = 0;
    for (int i = 1; i < numLines + 1; i++) {
        if (nums[i + 1] - nums[i - 1] >= 4) {
            mustVisit[index] = i;
            index++;
        }
    }

    for (int i = 0; i < numReq; i++) {
        count *= findArrangements(&nums[0], mustVisit[i], mustVisit[i + 1]);
    }

    printf("Total number of distinct arrangements: %lli\n", count);

	printf("\nProgram Done");

	return 1;
}
