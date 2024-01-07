#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#define fileName "input.txt"
#define dataLine 200

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

int readData(int *bus) {
    int lineNum = 0, start, index = 0;
	char textRead[dataLine], *p;

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        if (lineNum == 0) {
            start = atoi(textRead);
        } else {
            p = strtok(textRead, ",");

            while (p) {
                if (isdigit(p[0]) != 0) {
                    bus[index] = atoi(p);
                    index++;
                }

                p = strtok(NULL, ",");
            }
        }

        lineNum++;
	}

	fclose(inFile);

    return start;
}

int numInstances(char *str, char character) {
    int count = 0;

    for (int i = 0; i < strlen(str); i++) {
        if (str[i] == character) {
            count++;
        }
    }

    return count;
}

int main () {
    int start, numBusses;

	char textRead[dataLine];

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        numBusses = numInstances(textRead, ',') + 1 - numInstances(textRead, 'x');
	}

	fclose(inFile);

	int busses[numBusses];

    start = readData(&busses[0]);

    int minWaited = 0;
    bool found = false;
    while (!found) {
        for (int i = 0; i < numBusses; i++) {
            if ((start + minWaited) % busses[i] == 0) {
                printf("Bus #%d arrives in %d minutes.\nAnswer: %d\n", busses[i], minWaited, busses[i] * minWaited);
                found = true;
            }
        }

        minWaited++;
    }



	printf("\nProgram Done");

	return 1;
}
