#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#define fileName "input.txt"
#define dataLine 150
#define nameLen 25

typedef struct field {
    char name[nameLen];
    int min[2], max[2];
} Field;

int findAmts(int *arr) {
    int numLines = 0, arrIndex = 0;
	char textRead[dataLine];

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        if (textRead[0] == '\n') {
            if (arrIndex >  0) {
                numLines--;
            }
            arr[arrIndex] = numLines;
            arrIndex++;
            numLines = 0;
        } else {
            ++numLines;
        }
	}

	fclose(inFile);

	return 1;
}

int readData(int *amts) {
    int count = 0, arrIndex = 0, index = 0;
	char textRead[dataLine], *p;
	struct field *fields;

	fields = calloc(amts[0], sizeof(Field));

	// Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        if (textRead[0] == '\n') {
            arrIndex++;
        } else if (arrIndex == 0) {
            p = strtok(textRead, ":");
            strcpy(fields[index].name, p);

            p = strtok(NULL, "-");
            fields[index].min[0] = atoi(p);
            p = strtok(NULL, " ");
            fields[index].max[0] = atoi(p);
            p = strtok(NULL, " ");

            p = strtok(NULL, "-");
            fields[index].min[1] = atoi(p);
            p = strtok(NULL, " ");
            fields[index].max[1] = atoi(p);

            printf("Field #%d named %s: %d-%d or %d-%d\n", index, fields[index].name, fields[index].min[0], fields[index].max[0], fields[index].min[1], fields[index].max[1]);


            index++;
        } else if (arrIndex == 2) {
            if (index == amts[0]) {
                index++;
                continue;
            }

            p = strtok(textRead, ",");

            while (p) {
                int val = atoi(p);
                bool valid = false;

                for (int i = 0; i < amts[0]; i++) {
                    if ((val >= fields[i].min[0] && val <= fields[i].max[0]) || (val >= fields[i].min[1] && val <= fields[i].max[1])) {
                        valid = true;
                        break;
                    }
                }

                if (!valid) {
                    count += val;
                }

                p = strtok(NULL, ",");
            }
        }
	}

	fclose(inFile);


    return count;
}


int main() {
    int amts[3];

    findAmts(&amts[0]);

    printf("Ticket scanning error rate: %d.\n", readData(&amts[0]));

    return 1;
}
