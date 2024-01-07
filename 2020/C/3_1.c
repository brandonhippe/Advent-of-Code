#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#define fileName "input.txt"
#define dataLine 33

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

int main () {
	int numLines, count = 0;
	int slope[2] = {3, 1};
	int loc[2] = {0, 0};

	numLines = findLines();

	if (numLines == -1) {
		printf("Error: could not open file. Quitting\n");
		return -1;
	}

	char textRead[dataLine];
	int lineNum = 0;

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	while(fgets(textRead, dataLine, inFile)) {
        int charIndex = loc[0] % (dataLine - 2);
        if (textRead[charIndex] == '#') {
            count++;
            textRead[charIndex] = 'X';
        } else {
            textRead[charIndex] = 'O';
        }

        printf("%s", textRead);

        loc[0] += slope[0];
        loc[1] += slope[1];
	}

	fclose(inFile);

    printf("Trees Hit: %d\n", count);

	printf("\nProgram Done");


	return 1;
}

