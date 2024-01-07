#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#define fileName "input.txt"
#define dataLine 100


typedef struct passport {
	int birth, issue, expiration, height, pid, cid;
	char hair[20], eyes[20];
} Passport;

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

void readData(struct passport *passports) {
    int i = 0;
	char textRead[dataLine], *p;

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        if (textRead[0] == '\n') {
            i++;
        }

        p = strtok(textRead, ":");

        while (p != NULL) {
            char field[5], data[20];
            strcpy(field, p);

            p = strtok(NULL, " ");
            if (p == NULL) {
                break;
            }
            strcpy(data, p);

            if (strncmp(field, "byr", 3) == 0) {
                passports[i].birth = atoi(data);
            } else if (strncmp(field, "iyr", 3) == 0) {
                passports[i].issue = atoi(data);
            } else if (strncmp(field, "eyr", 3) == 0) {
                passports[i].expiration = atoi(data);
            } else if (strncmp(field, "hgt", 3) == 0) {
                passports[i].height = atoi(data);
            } else if (strncmp(field, "hcl", 3) == 0) {
                strcpy(passports[i].hair, data);
            } else if (strncmp(field, "ecl", 3) == 0) {
                strcpy(passports[i].eyes, data);
            } else if (strncmp(field, "pid", 3) == 0) {
                passports[i].pid = atoi(data);
            } else if (strncmp(field, "cid", 3) == 0) {
                passports[i].cid = atoi(data);
            }

            p = strtok(NULL, ":");
        }
	}

	fclose(inFile);

    return;
}

bool valid(struct passport *passports, int i) {
    if (passports[i].birth == -1) {
        return false;
    } else if (passports[i].pid == -1) {
        return false;
    } else if (passports[i].issue == -1) {
        return false;
    } else if (passports[i].expiration == -1) {
        return false;
    } else if (passports[i].height == -1) {
        return false;
    } else if ((strcmp(passports[i].eyes, "\n")) == 0) {
        return false;
    } else if ((strcmp(passports[i].hair, "\n")) == 0) {
        return false;
    }

    return true;
}

int main () {
	int numLines, count = 0;
	struct passport *passports;

	numLines = findLines();

    passports = (Passport *)calloc(numLines, sizeof(Passport));
    for (int i = 0; i < numLines; i++) {
        passports[i].birth = -1;
        passports[i].cid = -1;
        passports[i].expiration = -1;
        strcpy(passports[i].eyes, "\n");
        strcpy(passports[i].hair, "\n");
        passports[i].height = -1;
        passports[i].issue = -1;
        passports[i].pid = -1;
    }

    readData(passports);

    /*
    for (int i = 0; i < numLines; i++) {
        printf("Birth: %d, Issue: %d, Exp: %d, Height: %d, Hair: %s, Eye: %s, PID: %d, CID: %d\n", passports[i].birth, passports[i].issue, passports[i].expiration, passports[i].height, passports[i].hair, passports[i].eyes, passports[i].pid, passports[i].cid);
    }
    */

    for (int i = 0; i < numLines; i++) {
        if (valid(passports, i)) {
            count++;
        }
    }

    printf("Valid: %d\n", count);

	printf("\nProgram Done");


	return 1;
}

