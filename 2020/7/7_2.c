#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#define fileName "input.txt"
#define dataLine 150
#define nameLen 25


struct bag *createBag(struct bag *b, char bagName[25], int arrLen, int *arr, char *amts);
void printBag(struct bag *b);
int findLines();
void readData(int *bags, int numBags, char *bagNames);
int getBagIndex(char *search, char *bagsList);
void getBagNames(char *bags);
int getAmount(char *amts, int index);
void findBagContents(char *inputText, int *arr, int arrIndex);
int numInstances(char *str, char character);
int canContain(struct bag *thisBag, int *bags);

typedef struct bag {
    char name[nameLen], amts[nameLen];
    int structSize, arrSize, contains[];
} Bag;

struct bag *createBag(struct bag *b, char bagName[25], int arrLen, int *arr, char *amounts) {
    b = malloc(sizeof(*b) + sizeof(int) * arrLen);

    strcpy(b->name, bagName);
    strcpy(b->amts, amounts);
    b->arrSize = arrLen;
    for (int i = 0; i < arrLen; i++) {
        b->contains[i] = *(arr + i);
    }

    b->structSize = (sizeof(*b) + sizeof(int) * arrLen);

    return b;
}

void printBag(struct bag *b) {
    printf("Bag color: %s\nContains bags", b->name);
    for (int i = 0; i < b->arrSize; i++) {
        printf("%s %dx%d", (i == 0 ? ":" : ","), b->contains[i], getAmount(b->amts, i));
    }

    printf("\n\n\n");
}

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

void readData(int *bags, int numBags, char *bagNames) {
    int lineNum = 0;
	char textRead[dataLine];

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return;
    }

	while(fgets(textRead, dataLine, inFile)) {
        int numContain = numInstances(textRead, ',') + 1, contains[numContain], index = 0, com = 0;
        contains[0] = -1;
        char bagName[nameLen] = "", *bagSearch, amts[nameLen] = "";
        bagSearch = (char *)calloc(nameLen, sizeof(char));


        char *p = strtok(textRead, " ");

        while (p) {

            if (strncmp(p, "bag", 3) == 0) {
                com++;
            }

            switch (com) {
                case 0:
                    strcat(bagName, p);
                    strcat(bagName, " ");
                    break;
                case 1:
                    bagName[strlen(bagName) - 1] = '\0';
                    com++;
                    break;
                case 2:
                    if (isdigit(p[0]) != 0) {
                        strcat(amts, p);
                        strcat(amts,",");
                        com++;
                    }
                    break;
                case 3:
                    strcat(bagSearch, p);
                    strcat(bagSearch, " ");
                    break;
                case 4:
                    bagSearch[strlen(bagSearch) - 1] = '\0';
                    contains[index] = getBagIndex(bagSearch, bagNames);
                    index++;
                    com = 2;
                    free(bagSearch);
                    bagSearch = (char *)calloc(nameLen, sizeof(char));
                    break;
            }

            p = strtok(NULL, " ");
        }

        amts[strlen(amts) - 1] = '\0';

        struct bag *temp = createBag(temp, bagName, numContain, &contains[0], amts);
        bags[lineNum] = temp;

        lineNum++;
	}

	fclose(inFile);

    return;
}

int getBagIndex(char *search, char *bagsList) {
    char text[strlen(search)], bagNames[strlen(bagsList)];

    strcpy(text, search);
    strcpy(bagNames, bagsList);

    int index = 0, prev = 0;
    bool found = false;

    for (int i = 0; i < strlen(bagNames); i++) {
        if (bagNames[i] == ',') {
            int strIndex = 0;
            char *temp;
            temp = (char *)calloc(i - prev, sizeof(char));

            for (int j = prev; j < i; j++) {
                temp[strIndex] = bagNames[j];
                strIndex++;
            }

            if (strncmp(search, temp, i - prev) == 0) {
                found = true;
                break;
            }

            prev = i + 1;
            index++;
        }
    }

    if (!found) {
        index = -1;
    }

    return index;
}

void getBagNames(char *bags) {
    int lineNum = 0;
	char textRead[dataLine], *p, *tempStr;

	tempStr = (char *)calloc(nameLen, sizeof(char));

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return;
    }

	while(fgets(textRead, dataLine, inFile)) {
        tempStr = (char *)realloc(tempStr, ((lineNum + 1) * (nameLen * sizeof(char))));
        p = strtok(textRead, " ");

        while (strncmp(p, "bags", 4) != 0) {
            strcat(tempStr, p);
            strcat(tempStr, " ");

            p = strtok(NULL, " ");
        }

        int tempLen = strlen(tempStr);
        tempStr[tempLen - 1] = ',';
        lineNum++;
	}

	fclose(inFile);

	strcpy(bags, tempStr);

    return;
}

int getAmount(char *amts, int index) {
    char text[strlen(amts)];
    strcpy(text, amts);

    char *p = strtok(text, ",");
    int i = 0;

    while (p) {
        if (i == index) {
            return (atoi(p));
        }

        i++;
        p = strtok(NULL, ",");
    }

    return -1;
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

int canContain(struct bag *thisBag, int *bags) {
    int count = 0;

    for (int i = 0; i < thisBag->arrSize; i++) {
        int indexAmt = getAmount(thisBag->amts, i);

        if (indexAmt > 0) {
            count += indexAmt * (1 + canContain(bags[thisBag->contains[i]], bags));
        }
    }

    return count;
}

int main () {
    int numLines, count;

	numLines = findLines();

	if (numLines == -1) {
        printf("Error: Could not read input file. Quitting\n");
        return -1;
	}

	char bagNames[numLines * nameLen];
	getBagNames(bagNames);

	int bags[numLines];

    readData(&bags[0], numLines, bagNames);

/*
    for (int i = 0; i < numLines; i++) {
        printBag(bags[i]);
    }
*/


    int index = getBagIndex("shiny gold", bagNames);
    count = canContain(bags[index], &bags[0]);


    printf("Number of bags that a shiny gold bag can contain: %d\n", count);


	printf("\nProgram Done");

	return 1;
}
