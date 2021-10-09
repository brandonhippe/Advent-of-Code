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
	int numLines, count, product = 1;
	int slope[2];
	int loc[2];

	numLines = findLines();

	if (numLines == -1) {
		printf("Error: could not open file. Quitting\n");
		return -1;
	}

    for (int i = 0; i < 5; i++) {
        if (i == 0) {
            slope[0] = 1;
            slope[1] = 1;
        } else if (i == 4) {
            slope[0] = 1;
            slope[1] = 2;
        } else {
            slope[0] += 2;
        }

        loc[0] = 0;
        loc[1] = 0;

        count = 0;

        char textRead[dataLine];
        int lineNum = -1;

        // Open the file
        FILE *inFile = fopen(fileName, "r");

        while(fgets(textRead, dataLine, inFile)) {
            lineNum++;
            if (lineNum != loc[1]) {
                continue;
            }
            int charIndex = loc[0] % (dataLine - 2);
            if (textRead[charIndex] == '#') {
                count++;
                textRead[charIndex] = 'X';
            } else {
                textRead[charIndex] = 'O';
            }

            //printf("%s", textRead);

            loc[0] += slope[0];
            loc[1] += slope[1];
        }

        fclose(inFile);

        printf("Trees Hit: %d\n", count);

        product *= count;
    }

    printf("Product: %d\n", product);

	printf("\nProgram Done");


	return 1;
}

