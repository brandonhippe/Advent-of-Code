#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#define fileName "input.txt"
#define dataLine 50

unsigned long long int applyBitmask(char *bitmask, unsigned long long int inp);
void uLtoBin(unsigned long long int inp, int *arr, int numBits);
unsigned long long int binToUL (int *arr, int numBits);

unsigned long long int findMaxAddr() {
	unsigned long int maxAddr = 0, addr;
	char textRead[dataLine], *p;

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        p = strtok(textRead, "[");

        if (p) {
            p = strtok(NULL, "]");
            addr = atoi(p);

            if (addr > maxAddr) {
                maxAddr = addr;
            }
        }
	}

	fclose(inFile);

	return maxAddr + 1;
}

void readData(unsigned long long int *memory) {
    unsigned long long int temp;
    unsigned int addr;
	char textRead[dataLine], bitmask[37], *p, *endp;

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return;
    }

	while(fgets(textRead, dataLine, inFile)) {
        if (textRead[1] == 'a') {
            p = strtok(textRead, " ");
            p = strtok(NULL, " ");
            p = strtok(NULL, "\n");
            strcpy(bitmask, p);
        } else {
            p = strtok(textRead, "[");
            p = strtok(NULL, "]");
            addr = atoi(p);

            p = strtok(NULL, " ");
            p = strtok(NULL, " ");
            temp = strtoul(p, &endp, 10);

            temp = applyBitmask(bitmask, temp);
            memory[addr] = temp;
        }
	}

	fclose(inFile);

    return;
}

unsigned long long int applyBitmask(char *bitmask, unsigned long long int inp) {
    int inpBin[36];
    uLtoBin(inp, &inpBin[0], 36);

    for (int i = 0; i < 36; i++) {
        if (bitmask[i] == '0') {
            inpBin[i] = 0;
        } else if (bitmask[i] == '1') {
            inpBin[i] = 1;
        }
    }

    inp = binToUL(&inpBin[0], 36);
    return inp;
}

void uLtoBin(unsigned long long int inp, int *arr, int numBits) {
    for (int i = 0; i < numBits && inp > 0; i++) {
        if (inp >= pow(2, 35 - i)) {
            inp -= (int) pow(2, 35 - i);
            arr[i] = 1;
        } else {
            arr[i] = 0;
        }
    }
}

unsigned long long int binToUL (int *arr, int numBits) {
    unsigned long long int result = 0;
    for (int i = 0; i < numBits; i++) {
        if (arr[i] == 1) {
            result += (unsigned long long int) pow(2, 35 - i);
        }
    }

    return result;
}

int main () {
    unsigned long long int memSum = 0, *memory, largestAddr = findMaxAddr();

    if (largestAddr < 0) {
        printf("Error: could not open file.\n");
        return -1;
    }

    memory = (unsigned long long int *)calloc(largestAddr, sizeof(unsigned long long int));

    readData(memory);

    for (unsigned int i = 0; i < largestAddr; i++) {
        memSum += memory[i];
        //printf("%lu\n", memory[i]);
    }
    printf("The sum of all values left in memory is: %llu\n", memSum);


	printf("\nProgram Done");

	return 1;
}
