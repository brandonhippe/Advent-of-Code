#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#define fileName "input.txt"
#define passwordLength 50
#define dataLine 100

typedef struct passwordInfo {
	char password[passwordLength];
	char character;
	int min;
	int max;
} PasswordInfo;

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

void readData(struct passwordInfo *passwords, int numLines){
	char textRead[dataLine], *p;
	int lineNum = 0;

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	while(fgets(textRead, dataLine, inFile)) {
		p = strtok(textRead, "-");
		int min = atoi(p);
		passwords[lineNum].min = min;

		p = strtok(NULL, " ");
		int max = atoi(p);
		passwords[lineNum].max = max;

		p = strtok(NULL, ":");
		char character = *p;
		passwords[lineNum].character = character;

		p = strtok(NULL, " ");
		strcpy(passwords[lineNum].password, p);

		++lineNum;
	}

	fclose(inFile);

	return;
}

int charCount(struct passwordInfo *passwords, int index) {
    int count = 0;
    char password[passwordLength];

    strcpy(password, passwords[index].password);
    for (int i = 0; i < passwordLength; i++) {
        char char1 = password[i];
        char char2 = passwords[index].character;
        if (passwords[index].password[i] == passwords[index].character) {
            count++;
        }
    }

    return count;
}

int main () {
	int numLines, countValid = 0;
	struct passwordInfo *passwords;

	numLines = findLines();

	if (numLines == -1) {
		printf("Error: could not open file. Quitting\n");
		return -1;
	}

	passwords = (PasswordInfo *)calloc(numLines, sizeof(PasswordInfo));

	readData(passwords, numLines);

    for (int i = 0; i < numLines; i++) {
        int count = charCount(passwords, i);
        if (count >= passwords[i].min && count <= passwords[i].max) {
            countValid++;
        }
    }

    printf("Valid Passwords: %d\n", countValid);

	printf("\nProgram Done");


	return 1;
}

