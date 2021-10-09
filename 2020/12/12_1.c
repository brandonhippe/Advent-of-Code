#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#define fileName "input.txt"
#define dataLine 10
#define PI 3.14159265

double degToRad(int deg);

typedef struct instruction {
    char action;
    int value;
} Instruction;

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

void readData(struct instruction *ins) {
    int lineNum = 0;
	char textRead[dataLine];

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return;
    }

	while(fgets(textRead, dataLine, inFile)) {
        ins[lineNum].action = textRead[0];
        char temp[strlen(textRead)];
        for (int i = 1; i < strlen(textRead); i++) {
            temp[i - 1] = textRead[i];
        }

        ins[lineNum].value = atoi(temp);

        lineNum++;
	}

	fclose(inFile);

    return;
}

void followIns(struct instruction *ins, int *loc, int numIns) {
    int orientation = 0;
    int newLoc[2] = {0, 0};
    for (int i = 0; i < numIns; i++){
        //printf("%c%d\n", ins[i].action, ins[i].value);
        char tempAction;
        switch (ins[i].action) {
            case 'F':
                if (orientation % 360 == 0) {
                    tempAction = 'E';
                } else if (orientation % 180 == 0) {
                    tempAction = 'W';
                }

                if ((orientation + 90) % 360 == 0) {
                    tempAction = 'S';
                } else if ((orientation + 90) % 180 == 0) {
                    tempAction = 'N';
                }
                break;
            default:
                tempAction = ins[i].action;
        }

        switch (tempAction) {
            case 'N':
                newLoc[1] += ins[i].value;
                break;
            case 'S':
                newLoc[1] -= ins[i].value;
                break;
            case 'E':
                newLoc[0] += ins[i].value;
                break;
            case 'W':
                newLoc[0] -= ins[i].value;
                break;
            case 'L':
                orientation += ins[i].value;
                break;
            case 'R':
                orientation -= ins[i].value;
                break;
        }
    }
    loc[0] = newLoc[0];
    loc[1] = newLoc[1];

    return;
}

int manhatDist(int *loc) {
    return(abs(loc[0]) + abs(loc[1]));
}

int main () {
    int numLines, loc[2] = {0, 0};
    struct instruction *ins;

	numLines = findLines();

	if (numLines == -1) {
        printf("Error: Could not read input file. Quitting\n");
        return -1;
	}

	ins = (Instruction *)calloc(numLines, sizeof(Instruction));

    readData(ins);

/*
    for (int i = 0; i < numLines; i++) {
        printf("%c%d\n", ins[i].action, ins[i].value);
    }
*/

    followIns(ins, &loc[0], numLines);

    printf("Manhattan Distance: %d\n", manhatDist(&loc[0]));


	printf("\nProgram Done");

	return 1;
}
