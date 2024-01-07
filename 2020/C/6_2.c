#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#define fileName "input.txt"
#define dataLine 30

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
        if (textRead[0] == '\n') {
            ++numLines;
        }
	}

	fclose(inFile);

	return numLines;
}

void groupSize(int *groups) {
    int group = 0, i = 0;
	char textRead[dataLine];

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        if (textRead[0] == '\n') {
            groups[i] = group;
            i++;
            group = 0;
        } else {
            group++;
        }
	}

	fclose(inFile);

    return;
}

int readData(int *groups) {
    int count = 0, lineNum = 0;
	char textRead[dataLine], *ans;

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return;
    }

    ans = (char *) malloc((groups[0] * dataLine) + 1);
    ans[0] = '\n';

	while(fgets(textRead, dataLine, inFile)) {
        if (textRead[0] == '\n') {
            for (int i = 97; i<= 122; i++) {
                if (charCount(ans, i) == groups[lineNum]) {
                    count++;
                }
            }

            lineNum++;
            free(ans);
            ans = (char *) malloc((groups[lineNum] * dataLine) + 1);
            ans[0] = '\n';
        } else {
            if (ans[0] == '\n') {
                strcpy(ans, textRead);
            } else {
                strcat(ans, textRead);
            }
        }
	}

	fclose(inFile);

    return count;
}

int charCount(char *str, int ch) {
    int count = 0;
    for (int i = 0; str[i] != '\0'; ++i) {
        if (ch == str[i])
            ++count;
    }

    return count;
}

int main () {
    int count, numLines;
	numLines = findLines();


	if (numLines == -1) {
        printf("Error: Could not read input file. Quitting\n");
        return -1;
	}

    int groups[numLines];
    groupSize(&groups[0]);

    count = readData(&groups[0]);

    printf("Sum of Counts: %d\n", count);

	printf("\nProgram Done");


	return 1;
}
