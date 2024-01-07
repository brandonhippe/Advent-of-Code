#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#define fileName "input.txt"
#define dataLine 30

int findLines() {
	int numLines = 1;
	char textRead[dataLine];

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        if (textRead[0] == '\n') {
            ++numLines;
        }
	}

	fclose(inFile);

	return numLines;
}

int readData() {
    int count = 0;
	char textRead[dataLine], ans[dataLine];
	for (int i = 0; i < dataLine; i++) {
        ans[i] = (i == 0) ? '\n' : ' ';
    }

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return;
    }

	while(fgets(textRead, dataLine, inFile)) {
        if (textRead[0] == '\n') {
            int i = 0;
            while (ans[i] != '\n') {
                count++;
                i++;
                printf("%c", ans[i]);
            }
            printf("\n");

            for (i = 0; i < dataLine; i++) {
                ans[i] = (i == 0) ? '\n' : ' ';
            }

            continue;
        }

        int i = 0;
        while (textRead[i] != '\n') {
            char *p;
            char temp = textRead[i];
            char temps[dataLine];
            strcpy(temps, ans);

            p = strchr(ans, textRead[i]);

            if (p == NULL) {
                p = strchr(ans, '\n');

                *p = temp;
                *(p + 1) = '\n';
            }

            i++;
        }
	}

	fclose(inFile);

    return count;
}

int main () {
    int count, numLines;
	numLines = findLines();

	if (numLines == -1) {
        printf("Error: Could not read input file. Quitting\n");
        return -1;
	}

    count = readData();


    printf("Sum of Counts: %d\n", count);

	printf("\nProgram Done");


	return 1;
}

