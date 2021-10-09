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

void swap(int *arr, int a, int b);

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

void followIns(struct instruction *ins, int *shipLoc, int *wayLoc, int numIns) {
    for (int i = 0; i < numIns; i++){
        //printf("%c%d\n", ins[i].action, ins[i].value);
        int temp;
        switch (ins[i].action) {
            case 'N':
                wayLoc[1] += ins[i].value;
                break;
            case 'S':
                wayLoc[1] -= ins[i].value;
                break;
            case 'E':
                wayLoc[0] += ins[i].value;
                break;
            case 'W':
                wayLoc[0] -= ins[i].value;
                break;
            case 'L':
                temp = ins[i].value;
                while (temp > 0) {
                    swap(wayLoc, 0, 1);
                    wayLoc[0] *= -1;
                    temp -= 90;
                }
                break;
            case 'R':
                temp = ins[i].value;
                while (temp > 0) {
                    swap(wayLoc, 0, 1);
                    wayLoc[1] *= -1;
                    temp -= 90;
                }
                break;
            case 'F':
                shipLoc[0] += (ins[i].value * wayLoc[0]);
                shipLoc[1] += (ins[i].value * wayLoc[1]);
                break;
        }
    }

    return;
}

void swap(int *arr, int a, int b) {
    int temp = arr[a];
    arr[a] = arr[b];
    arr[b] = temp;
    return;
}

int manhatDist(int *loc) {
    return(abs(loc[0]) + abs(loc[1]));
}

int main () {
    int numLines, shipLoc[2] = {0, 0}, wayLoc[2] = {10, 1};
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

    followIns(ins, &shipLoc[0], &wayLoc[0], numLines);

    printf("Manhattan Distance: %d\n", manhatDist(&shipLoc[0]));


	printf("\nProgram Done");

	return 1;
}
