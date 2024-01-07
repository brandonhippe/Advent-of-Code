#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#define fileName "input2.txt"
#define dataLine 200


typedef struct rule {
    int num, len[2], subRules[6], pipe;
    char text[dataLine];
    bool selfReferential;
} Rule;

int countChar(char *str, char search) {
    int i = 0, count = 0;
    while (i < strlen(str)) {
        count += (str[i] == search) ? 1 : 0;
        i++;
    }

    return count;
}

struct rule *createRule(struct rule *r, int ruleNum, char *otherRules) {
    r->num = ruleNum;
    r->selfReferential = false;
    strncpy(r->text, otherRules, strlen(otherRules) - 1);

    for (int i = 0; i < 6; i++) {
        r->subRules[i] = 0;
        r->len[i % 2] = 0;
    }
    r->pipe = 5;

    char *p = strchr(otherRules, '|');
    if (p) {
        p = strtok(otherRules, "|");
        r->pipe = countChar(p, ' ');
    }

    return r;
}

int getLength(struct rule *r) {
    if (r->len[0] == 0 && r->len[1] == 0) {
        if (isalpha(r->text[0]) != 0) {
            r->len[0] = 1;
            r->len[1] = 1;
        } else {
            int index = 0;
            struct rule *r1 = r->subRules[index];
            while (r1) {
                if (r1 != r) {
                    int temp = getLength(r1);
                    if (temp == -1) {
                        r->len[0] = -1;
                        r->len[1] = -1;
                    } else if (r->pipe == 5) {
                        r->len[0] += temp;
                        r->len[1] += temp;
                    } else {
                        r->len[index >= r->pipe ? 1 : 0] += temp;
                    }
                }

                index++;
                r1 = r->subRules[index];
            }
        }
    }

    if (r->len[0] != r->len[1] || r->selfReferential) {
        return -1;
    }

    return r->len[0];
}

bool fits(struct rule *r, char *check) {
    int l[2] = {strlen(check), r->len[0]}, Rnum = r->num;
    if (l[0] < l[1] || (!r->selfReferential && l[0] != l[1])) {
        return false;
    }

    if (isalpha(r->text[0]) != 0) {
        return check[0] == r->text[0];
    } else {
        int i = 0, charIndex = 0;
        struct rule *r1 = r->subRules[i];
        bool reset = false, fit = true;
        while (r1) {
            int length;
            char *temp, *p = check + (charIndex * sizeof(char));

            if (r1 == r) {
                struct rule *next = r->subRules[i + 1];

                length = strlen(p) - ((next) ? next->len[0] : 0);
            } else if (i == r->pipe - 1) {
                length = strlen(p);
            }  else {
                length = r1->len[i >= r->pipe ? 1 : 0];
            }

            temp = (char*)calloc(length + 1, sizeof(char));
            strncpy(temp, p, length);

            if (!fits(r1, temp)) {
                if (i < r->pipe && r->pipe != 5) {
                    i = r->pipe - 1;
                    fit = false;
                } else {
                    return false;
                }
            }

            charIndex += length;
            i++;
            r1 = r->subRules[i];

            if (i >= r->pipe && !reset) {
                if (fit) {
                    return true;
                } else {
                    charIndex = 0;
                    reset = true;
                }
            }
        }
    }

    return true;
}

bool fitsR0(struct rule *r, char *check) {
    struct rule *s0, *s1;
    s0 = r->subRules[0];
    s1 = r->subRules[1];

    for (int i = s0->len[0]; i < strlen(check); i += s0->len[0]) {
        if ((strlen(check) - i) % s1->len[0] == 0) {
            char *p0, *p1;
            p0 = (char*)calloc(i + 1, sizeof(char));
            p1 = (char*)calloc((strlen(check) - i) + 1, sizeof(char));

            strncpy(p0, check, i);
            strncpy(p1, check + i, strlen(check) - i);

            if (fits(s0, p0) && fits(s1, p1)) {
                return true;
            }
        }
    }


    return false;
}

void printRule(struct rule *r) {
    printf("Rule #%d: %s\n", r->num, r->text);

    if (r->pipe != 5) {
        printf("Before pipe: %d\n", r->pipe);
    }
    if (r->len[0] == -1) {
        printf("Paths to rule have different lengths!\n\n");
    } else {
        printf("Length: %d, %d\n\n", r->len[0], r->len[1]);
    }
/*
    int i = 0;
    while (r->subRules[i] != 0) {
        printf("%d ", r->subRules[i]);
        i++;
    }

    printf("\n");
*/
    return;
}

int main() {
    int numRules = 0;
    bool inRules = true;
    char *textRead = (char*)calloc(dataLine, sizeof(char));
    // Open the file
	FILE *inFile = fopen(fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        if (textRead[0] == '\n') {
            inRules = false;
        }

        if (inRules) {
            numRules++;
        }

        free(textRead);
        textRead = (char*)calloc(dataLine, sizeof(char));
	}

	fclose(inFile);

	int *rules = (int*)calloc(numRules, sizeof(struct rule));


    inFile = fopen(fileName, "r");
    inRules = true;
    textRead = (char*)calloc(dataLine, sizeof(char));
    int index = 0;

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        if (textRead[0] == '\n') {
            inRules = false;
        }

        if (inRules) {
            char *contains = strchr(textRead, ' ');
            contains += sizeof(char);
            int ruleNum = round(strtof(textRead, NULL));

            struct rule *temp = (struct rule*)calloc(1, sizeof(struct rule));
            temp = createRule(temp, ruleNum, contains);
            rules[index] = temp;
            index++;
        }

        free(textRead);
        textRead = (char*)calloc(dataLine, sizeof(char));
	}

	fclose(inFile);

	for (int i = 0; i < numRules; i++) {
        struct rule *r = rules[i];
        char *temp = (char*)calloc(strlen(r->text) + 1, sizeof(char));
        strcpy(temp, r->text);

        char *p = strtok(temp, " ");
        index = 0;

        while (p) {
            if (p[0] != '|') {
                int subRule = atoi(p);

                for (int j = 0; j < numRules; j++) {
                    struct rule *r1 = rules[j];
                    if (r1->num == subRule) {
                        if (i == j) {
                            r->selfReferential = true;
                        }

                        r->subRules[index] = r1;
                        index++;
                        break;
                    }
                }
            }

            p = strtok(NULL, " ");
        }
	}

	struct rule *r0;

	for (int i = 0; i < numRules; i++) {
        struct rule *r = rules[i];
        if (r->num == 0) {
            r0 = r;
        }
	}

	getLength(r0);

	for (int i = 0; i < numRules; i++) {
        struct rule *temp = rules[i];
        printRule(temp);
	}

	for (int i = 0; i < numRules; i++) {
        struct rule *temp = rules[i];
        if (temp->len[0] == -1 && temp->num != 0) {
            return -1;
        }
	}

	inFile = fopen(fileName, "r");
    inRules = true;
    textRead = (char*)calloc(dataLine, sizeof(char));
    int count = 0;

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        if (textRead[0] == '\n') {
            inRules = false;
        } else if (!inRules) {
            textRead[strlen(textRead) - 1] = 0;
            bool stringFits = fitsR0(r0, textRead);
            count += stringFits ? 1 : 0;
        }

        free(textRead);
        textRead = (char*)calloc(dataLine, sizeof(char));
	}

	fclose(inFile);

	printf("Number of lines that are valid: %d\n", count);

    return 1;
}
