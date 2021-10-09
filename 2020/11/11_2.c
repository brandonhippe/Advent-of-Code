#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#define fileName "input.txt"
#define dataLine 105

int findLines(int *len) {
	int numLines = 0;
	char textRead[dataLine];

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        *len = strlen(textRead);
        ++numLines;
	}

	fclose(inFile);

	return numLines;
}

void readData(int *nums, int line) {
    int lineNum = 0, index;
	char textRead[dataLine];

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return;
    }

	while(fgets(textRead, dataLine, inFile)) {
        index = 0;
        while (textRead[index] != '\n') {
            switch (textRead[index]) {
                case 'L':
                    *(nums + (line * lineNum) + index) = -1;
                    break;
                case '.':
                    *(nums + (line * lineNum) + index) = 0;
                    break;
            }

            index++;
        }

        lineNum++;
	}

	fclose(inFile);

    return;
}

bool iterate(int *seats, int lines, int line) {
    int newSeats[lines][line];
    bool changed = false;


    for (int i = 0; i < lines; i++) {
        for (int j = 0; j < line; j++) {
            if (*(seats + (line * i) + j) == 0) {
                newSeats[i][j] = 0;
                continue;
            }

            int surr = 0;
            for (int m = -1; m <= 1; m++) {
                for (int n = -1; n <= 1; n++) {
                    if (m == 0 && n == 0) {
                        continue;
                    }

                    int mult = 1;
                    while (i + (m * mult) >= 0 && i + (m * mult) < lines && j + (n * mult) >= 0 && j + (n * mult) < line) {
                        if (*(seats + (line * (i + (m * mult))) + (j + (n * mult))) != 0) {
                            if (*(seats + (line * (i + (m * mult))) + (j + (n * mult))) > 0) {
                                surr++;
                            }
                            break;
                        }
                        mult++;
                    }
                }
            }

            if (((*(seats + (line * i) + j) < 0) && surr == 0) || ((*(seats + (line * i) + j) > 0) && surr >= 5)) {
                newSeats[i][j] = *(seats + (line * i) + j) * -1;
                changed = true;
            } else {
                newSeats[i][j] = *(seats + (line * i) + j);
            }
        }
    }

    cpyArr(seats, &newSeats[0][0], lines * line);

    return changed;
}

void cpyArr(int *arr1, int *arr2, int size) {
    for (int i = 0; i < size; i++) {
        *(arr1 + i) = *(arr2 + i);
    }

    return;
}

int countOcc(int *arr, int size) {
    int count = 0;
    for (int i = 0; i < size; i++) {
        if (*(arr + i) > 0) {
            count++;
        }
    }

    return count;
}

void printSeats(int *seats, int numLines, int line) {
    for (int i = 0; i < numLines; i++) {
        for (int j = 0; j < line; j++) {
            printf("%s", (*(seats + (line * i) + j) > 0) ? "#" : ((*(seats + (line * i) + j) < 0) ? "L" : "."));
        }
        printf("\n");
    }

    printf("\n\n");

    return;
}

int main () {
    int numLines, len = 0;
    bool changed;
	numLines = findLines(&len);

	if (numLines == -1) {
        printf("Error: Could not read input file. Quitting\n");
        return -1;
	}

	int seats[numLines][len], tempSeats[numLines][len];

	readData(&seats[0][0], len);

    //printSeats(&seats[0][0], numLines, len);


	do {
        changed = iterate(&seats[0][0], numLines, len);

        //printf("Number of occupied seats: %d\n", countOcc(&(seats[0][0]), numLines * len));
        //printSeats(&seats[0][0], numLines, len);
	} while (changed);

	//!cmpArr(&seats[0][0], &tempSeats[0][0], numLines * len)

    printf("Number of occupied seats: %d\n", countOcc(&(seats[0][0]), numLines * len));

	printf("\nProgram Done");

	return 1;
}
