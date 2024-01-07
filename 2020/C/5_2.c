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
	int numLines, count = 0, seat;

	numLines = findLines();

	if (numLines == -1) {
        printf("Error: Could not read input file. Quitting\n");
        return -1;
	}

    int seats[numLines];

    readData(&seats[0]);

    quickSort(&seats[0], 0, numLines - 1);

    seat = seats[0] + 1;
    for (int i = 1; i < numLines; i++) {
        if ((seats[i] == seat + 1) && (seats[i - 1] == seat - 1)) {
            break;
        }

        seat++;
    }

    printf("Your seat: %d\n", seat);

	printf("\nProgram Done");


	return 1;
}

