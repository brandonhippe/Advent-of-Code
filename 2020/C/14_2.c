#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#define fileName "input.txt"
#define dataLine 50

void uLtoBin(unsigned long long int inp, int *arr, int numBits);
unsigned long long int binToUL (int *arr, int numBits);
int countChar(char *mask, char id);


unsigned long long int findAddr() {
    unsigned long long int numAddr = 0;
	char textRead[dataLine], *p, bitmask[dataLine];

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

    while(fgets(textRead, dataLine, inFile)) {
        if (textRead[1] == 'a') {
            p = strtok(textRead, " ");
            p = strtok(NULL, " ");
            p = strtok(NULL, "\n");
            strcpy(bitmask, p);
        } else {
            numAddr += pow(2, countChar(bitmask, 'X'));
        }
	}

	fclose(inFile);

    return numAddr;
}

int countChar(char *bitmask, char id) {
    int count = 0;
    for (int i = 0; i < dataLine; i++) {
        if (bitmask[i] == id) {
            count++;
        }
    }

    return count;
}


int readData(unsigned long long int *memAddrs, unsigned long long int *memVals, int numAddr) {
    unsigned long long int val, addr;
	char textRead[dataLine], bitmask[37], *p, *endp;
	int addrsAssigned = 0;

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
            addr = strtoul(p, &endp, 10);

            int change = pow(2, countChar(bitmask, 'X'));
            unsigned long long int addrs[change];
            applyBitmask(bitmask, addr, &addrs[0], change);

            p = strtok(NULL, " ");
            p = strtok(NULL, " ");
            val = strtoul(p, &endp, 10);

            for (int i = 0; i < change; i++) {
                int index = findIndex(addrs[i], memAddrs, addrsAssigned);

                if (index < 0) {
                    memAddrs[addrsAssigned] = addrs[i];
                    index = addrsAssigned;
                    addrsAssigned++;
                }

                memVals[index] = val;
            }

        }
	}

	fclose(inFile);

    return addrsAssigned;
}


void applyBitmask(char *bitmask, unsigned long long int addr, unsigned long long int *addrs, int num) {
    int addrBin[36], locs[countChar(bitmask, 'X')], found = 0;
    uLtoBin(addr, &addrBin[0], 36);

    for (int i = 0; i < 36; i++) {
        if (bitmask[i] == '1') {
            addrBin[i] = 1;
        } else if (bitmask[i] == 'X') {
            locs[found] = i;
            found++;
            addrBin[i] = 0;
        }
    }

    for (int i = 0; i < num; i++) {
        int temp = i, pos = 0;

        while (temp > 0) {
            addrBin[locs[pos]] = temp % 2;
            temp /= 2;
            pos++;
        }

        addrs[i] = binToUL(&addrBin[0], 36);
    }

    return;
}

int findIndex(unsigned long long int addrs, unsigned long long int *memAddrs, int num) {
    int index = -1;

    for (int i = 0; i < num; i++) {
        if (memAddrs[i] == addrs) {
            index = i;
            break;
        }
    }

    return index;
}


void uLtoBin(unsigned long long int inp, int *arr, int numBits) {
    for (int i = 0; i < numBits; i++) {
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
    unsigned long long int numAddr = findAddr();


    unsigned long long int memAddrs[numAddr], memVals[numAddr];

    for (int i = 0; i < numAddr; i++) {
        memAddrs[i] = 0;
        memVals[i] = 0;
    }

    int assigned = readData(&memAddrs[0], &memVals[0], numAddr);

    unsigned long long int memSum = 0;

    for (int i = 0; i < assigned; i++) {
        //printf("Address: %llu Value: %llu\n", memAddrs[i], memVals[i]);
        memSum += memVals[i];
    }


    printf("The sum of all values left in memory is: %llu\n", memSum);


	printf("\nProgram Done");

	return 1;
}
