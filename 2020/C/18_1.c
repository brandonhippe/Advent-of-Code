#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#define fileName "input.txt"
#define dataLine 200

void replaceStr(char *dest, char *src1, char *src2, int start, int end) {
    strncat(dest, src1, start);
    strcat(dest, src2);

    int i = strlen(dest), index = end;

    while (index < strlen(src1)) {
        dest[i] = src1[index];
        i++;
        index++;
    }

    return;
}


unsigned long long int collapse(char *str) {
    char *p = strchr(str, '(');

    while (p) {
        int dist = 0, openCount = 0;

        do {
            if (p[dist] == '(') {
                openCount++;
            } else if (p[dist] == ')') {
                openCount--;
            }

            dist++;
        } while (openCount != 0);

        char *paren = (char*)calloc(dist - 1, sizeof(char));
        strncpy(paren, p + sizeof(char), dist - 2);

        unsigned long long int rep = collapse(paren);
        char *repStr = (char*)calloc((int)(log10(rep) + 1) + 1, sizeof(char));
        sprintf(repStr, "%llu", rep);

        int fIndex = 0;
        while (str[fIndex] != '(') {
            fIndex++;
        }
        char *next = (char*)calloc(strlen(str), sizeof(char));
        replaceStr(next, str, repStr, fIndex, fIndex + dist);
        strcpy(str, next);

        p = strchr(str, '(');
    }

    unsigned long long int count = 0;
    char Op = '+';

    p = strtok(str, " ");
    while (p) {
        if (isdigit(p[0]) == 0) {
            Op = p[0];
        } else {
            if (Op == '+') {
                count += strtoull(p, NULL, 10);
            } else {
                count *= strtoull(p, NULL, 10);
            }
        }

        p = strtok(NULL, " ");
    }

    return count;
}

int main() {
    unsigned long long int count = 0;
    char *textRead = (char*)calloc(dataLine, sizeof(char));

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

    unsigned long long int pCount = count;
    int line = 0;
	while(fgets(textRead, dataLine, inFile)) {
        unsigned long long int temp = collapse(textRead);
        count = count + temp;
        //printf("#%d: %llu\n", line + 1, temp);

        line++;

        free(textRead);
        textRead = (char*)calloc(dataLine, sizeof(char));
        pCount = count;
	}

	fclose(inFile);

	printf("Count: %llu\n", count);

    return 1;
}
