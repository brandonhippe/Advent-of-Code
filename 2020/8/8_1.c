#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#define fileName "input.txt"
#define dataLine 15

int acc;

typedef struct code {
	int num, op;
	bool visited;
} Code;

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

void readData(struct code *codeLines) {
    int lineNum = 0;
	char textRead[dataLine], *p;

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return;
    }

	while(fgets(textRead, dataLine, inFile)) {
        p = strtok(textRead, " ");

        if (strncmp(textRead, "nop", 3) == 0) {
            codeLines[lineNum].op = 1;
        } else if (strncmp(textRead, "acc", 3) == 0) {
            codeLines[lineNum].op = 0;
        } else if (strncmp(textRead, "jmp", 3) == 0) {
            codeLines[lineNum].op = -1;
        }

        p = strtok(NULL, "\n");

        codeLines[lineNum].num = atoi(p);
        codeLines[lineNum].visited = false;

        lineNum++;
	}

	fclose(inFile);

    return;
}

bool runCode(struct code *codeLines, int lineNum, int numLines) {
    if (lineNum >= numLines) {
        return true;
    }

    if (codeLines[lineNum].visited) {
        return false;
    }

    codeLines[lineNum].visited = true;

    switch (codeLines[lineNum].op) {
        case -1:
            lineNum += codeLines[lineNum].num;
            break;
        case 0:
            acc += codeLines[lineNum].num;
        default:
            lineNum++;
    }

    return runCode(codeLines, lineNum, numLines);
}

int main () {
    int numLines;
    struct code *codeLines;
	numLines = findLines();

	if (numLines == -1) {
        printf("Error: Could not read input file. Quitting\n");
        return -1;
	}

	codeLines = (Code *)calloc(numLines, sizeof(Code));

    readData(codeLines);

    runCode(codeLines, 0, numLines);

    printf("Accumulator: %d\n", acc);

	printf("\nProgram Done");


	return 1;
}
