#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#define fileName "input.txt"
#define dataLine 200


/*
    *** INPUT MUST BE CHANGED TO REMOVE THE FIRST LINE ***
*/

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

void readData(int *bus) {
    int lineNum = 0, start, index = 0;
	char textRead[dataLine], *p;

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return;
    }

	while(fgets(textRead, dataLine, inFile)) {
        p = strtok(textRead, ",");

        while (p) {
            if (isdigit(p[0]) != 0) {
                bus[index] = atoi(p);
            } else {
                bus[index] = 1;
            }

            index++;

            p = strtok(NULL, ",");
        }

        lineNum++;
	}

	fclose(inFile);

    return;
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

int lcm(int *arr, int numEntries) {
    int arrCpy[numEntries];

    for (int i = 0; i < numEntries; i++) {
        arrCpy[i] = arr[i];
    }

    int divisor = 1;
    bool found = false;
    while (!found && divisor < findMax(&arrCpy[0], numEntries)) {
        found = true;
        divisor++;
        for (int i = 0; i < numEntries; i++) {
            if (arrCpy[i] % divisor != 0) {
                found = false;
            }
        }
    }

    if (found) {
        for (int i = 0; i < numEntries; i++) {
            if (arrCpy[i] != 1) {
                arrCpy[i] /= divisor;
            }
        }

        return lcm(&arrCpy[0], numEntries);
    } else {
        int product = 1;
        for (int i = 0; i < numEntries; i++) {
            product *= arrCpy[i];
        }

        return product;
    }
}

int findMax(int *arr, int numEntries) {
    int max = arr[0];
    for (int i = 1; i < numEntries; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }

    return max;
}

long long int firstAlignment(int *bus, int *indecies, int numEntries) {
    long long int time = 0;
    int tempArr[numEntries], offsets[numEntries];
    for (int i = 0; i < numEntries; i++) {
        tempArr[i] = bus[indecies[i]];
    }

    int stepSize = findMax(&tempArr[0], numEntries);
    int maxIndex;
    for (maxIndex = 0; maxIndex < numEntries; maxIndex++) {
        if (bus[indecies[maxIndex]] == stepSize) {
            break;
        }
    }

    for (int i = 0; i < numEntries; i++) {
        offsets[i] = indecies[i] - indecies[maxIndex];
    }

    bool found = false;
    while (!found) {
        found = true;
        time += stepSize;

        for (int i = 0; i < numEntries; i++) {
            if ((time + offsets[i]) % bus[indecies[i]] != 0) {
                found = false;
                break;
            }
        }
    }

    return time - indecies[maxIndex];
}

int main () {
    int numBusses;

	char textRead[dataLine];

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        numBusses = numInstances(textRead, ',') + 1;
	}

	fclose(inFile);

	int busses[numBusses];

    readData(&busses[0]);

    int stepSize = 1, indecies[3];
    for (int i = 0; i < numBusses - 2; i++) {
        for (int j = i + 1; j < numBusses - 1; j++) {
            for (int k = j + 1; k < numBusses; k++) {
                int tempArr[3] = {busses[i], busses[j], busses[k]};
                int temp = lcm(&tempArr[0], 3);
                if (temp > stepSize) {
                    stepSize = temp;
                    indecies[0] = i;
                    indecies[1] = j;
                    indecies[2] = k;
                }
            }
        }
    }

    long long int time = firstAlignment(&busses[0], &indecies[0], 3) - stepSize;

    bool found = false;
    while (!found) {
        found = true;
        time += stepSize;

        for (int i = 0; i < numBusses; i++) {
            if ((time + i) % busses[i] != 0) {
                found = false;
                break;
            }
        }
    }

    printf("The first time subsequent busses arrive at subsequent minutes is: %lli\n", time);


	printf("\nProgram Done");

	return 1;
}
