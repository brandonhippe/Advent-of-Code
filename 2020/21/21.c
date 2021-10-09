#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#define realData "input.txt"
#define testData "input1.txt"
#define dataLine 600
#define test false


typedef struct food {
    char ingredients[dataLine], allergens[dataLine];
    int aP[5];
} Food;

typedef struct allergen {
    char name[50];
    int foods[50], ing;
} Allergen;

typedef struct ingredient {
    char name[50];
    int foods[50], pAllergen[10];
} Ingredient;

typedef struct alphaPtr {
    int value;
    char name[50];
} AlphaPtr;

struct food *createFood(struct food *f, char *ing, char *all) {
    for (int i = 0; i < 5; i++) {
        f->aP[i] = 0;
    }

    strcpy(f->ingredients, ing);
    strcpy(f->allergens, all);

    return f;
}

void printFood(struct food *f) {
    if (f) {
        printf("Address: %d\nIngredients: %s\nKnown Allergens: %s\n\n\n", f, f->ingredients, f->allergens);
    } else {
        printf("***NULL FOOD***\n\n\n");
    }

    return;
}

struct allergen *createAllergen(struct allergen *a, char *name) {
    for (int i = 0; i < 50; i++) {
        a->foods[i] = 0;
    }

    a->ing = 0;

    strcpy(a->name, name);

    return a;
}

void printAllergen(struct allergen *a) {
    if (a) {
        printf("Allergen: %s\nFoods: ", a->name);

        int index = 0;
        while (a->foods[index] != 0) {
            if (index != 0) {
                printf(", ");
            }

            printf("%d", a->foods[index]);
            index++;
        }
    } else {
        printf("***NULL ALLERGEN***");
    }

    printf("\n\n\n");

    return;
}

struct ingredient *createIngredient(struct ingredient *ing, char *name, int* allergenArr) {
    for (int i = 0; i < 50; i++) {
        ing->foods[i] = 0;
        ing->pAllergen[i % 10] = allergenArr[i % 10];
    }

    strcpy(ing->name, name);

    return ing;
}

void printIngredient(struct ingredient *ing) {
    if (ing) {
        printf("Ingredient: %s\nFoods: ", ing->name);

        int index = 0;
        while (ing->foods[index] != 0) {
            if (index != 0) {
                printf(", ");
            }

            printf("%d", ing->foods[index]);
            index++;
        }

        index = 0;
        printf("\nPossible Allergens: ");
        while (ing->pAllergen[index] != 0) {
            if (index != 0) {
                printf(", ");
            }

            struct allergen *a = ing->pAllergen[index];
            printf("%s", a->name);
            index++;
        }
    } else {
        printf("***NULL INGREDIENT***");
    }

    printf("\n\n\n");

    return;
}

struct alphaPtr *createPtr(struct alphaPtr *a, int val, char *all) {
    a->value = val;
    strcpy(a->name, all);

    return a;
}

bool inCSV(char *check, char *csv) {
    char *temp = (char*)calloc(strlen(csv), sizeof(char)), *p = csv;
    while (strlen(p) != 0) {
        while (p[0] != ',' && strlen(p) != 0) {
            strncat(temp, p, 1);
            p++;
        }

        if (strcmp(temp, check) == 0) {
            return true;
        }

        if (strlen(p) != 0) {
            p++;
            temp = (char*)calloc(strlen(csv), sizeof(char));
        }
    }

    return false;
}

int numLines() {
	char textRead[dataLine];
	int size = 0;

	// Open the file
	FILE *inFile = fopen((test) ? testData : realData, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return -1;
    }

	while(fgets(textRead, dataLine, inFile)) {
        size++;
	}

	fclose(inFile);

	return size;
}

void readData(int *foods) {
	char textRead[dataLine];
	int size = 0;

	// Open the file
	FILE *inFile = fopen((test) ? testData : realData, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return;
    }

	while(fgets(textRead, dataLine, inFile)) {
        char *p = strchr(textRead, '(');
        char *q = strtok(p, " ");
        q = strtok(NULL, " ");
        char *all = (char*)calloc(strlen(p), sizeof(char)), *ing = (char*)calloc(dataLine - strlen(p), sizeof(char));

        while (q) {
            int len = strlen(q);
            if (q[len - 1] == '\n') {
                len -= 2;
            }

            strncat(all, q, len);

            q = strtok(NULL, " ");
        }


        p = strtok(textRead, " ");
        bool started = false;

        while (p[0] != '(') {
            if (started) {
                strcat(ing, ",");
            } else {
                started = true;
            }

            strcat(ing, p);
            p = strtok(NULL, " ");
        }

        struct food *f = (struct food*)calloc(1, sizeof(struct food));
        f = createFood(f, ing, all);
        foods[size] = f;
        size++;
	}

	fclose(inFile);

	return;
}

char *findAllergens(int *foods, int numFoods) {
    char *allergenNames = (char*)calloc(1, sizeof(char));

    for (int i = 0; i < numFoods; i++) {
        struct food *f = foods[i];
        char *fAll = (char*)calloc(strlen(f->allergens), sizeof(char));
        strcpy(fAll, f->allergens);
        char *temp = strtok(fAll, ",");

        while (temp) {
            if (!inCSV(temp, allergenNames)) {
                int pLen = strlen(allergenNames);
                allergenNames = (char*)realloc(allergenNames, strlen(allergenNames) + strlen(temp) + 2);

                if (pLen != 0) {
                    strcat(allergenNames, ",");
                }

                strcat(allergenNames, temp);
            }

            temp = strtok(NULL, ",");
        }
    }


    return allergenNames;
}

void genAllergens(char *allergenNames, int *allergens, int *foods, int numAllergens, int numFoods) {
    int allIndex = 0;
    char *curr = strtok(allergenNames, ",");

    while (curr) {
        struct allergen *a = (struct allergen*)calloc(1, sizeof(struct allergen));
        a = createAllergen(a, curr);
        allergens[allIndex] = a;

        int index = 0;
        for (int i = 0; i < numFoods; i++) {
            struct food *f = foods[i];
            char *fAll = (char*)calloc(strlen(f->allergens), sizeof(char));
            strcpy(fAll, f->allergens);

            if (inCSV(curr, fAll)) {
                a->foods[index] = f;
                index++;
            }
        }

        curr = strtok(NULL, ",");
        allIndex++;
    }

    return;
}

char *findIngredients(int *foods, int numFoods) {
    char *ingredientNames = (char*)calloc(1, sizeof(char));

    for (int i = 0; i < numFoods; i++) {
        struct food *f = foods[i];
        char *fIng = (char*)calloc(strlen(f->ingredients), sizeof(char));
        strcpy(fIng, f->ingredients);
        char *temp = strtok(fIng, ",");

        while (temp) {
            char *start = ingredientNames, *p = start;

            if (!inCSV(temp, ingredientNames)) {
                int pLen = strlen(ingredientNames);
                ingredientNames = (char*)realloc(ingredientNames, strlen(ingredientNames) + strlen(temp) + 2);

                if (pLen != 0) {
                    strcat(ingredientNames, ",");
                }

                strcat(ingredientNames, temp);
            }

            temp = strtok(NULL, ",");
        }
    }


    return ingredientNames;
}

void genIngredients(char *ingredientNames, int *ingredients, int *foods, int *allergens, int numIngredients, int numFoods, int numAllergens) {
    int *allergenArr = (int*)calloc(10, sizeof(int));
    for (int i = 0; i < numAllergens; i++) {
        allergenArr[i] = allergens[i];
    }

    int ingIndex = 0;
    char *curr = strtok(ingredientNames, ",");

    while (curr) {
        struct ingredient *ing = (struct ingredient*)calloc(1, sizeof(struct ingredient));
        ing = createIngredient(ing, curr, allergenArr);
        ingredients[ingIndex] = ing;

        int index = 0;
        for (int i = 0; i < numFoods; i++) {
            struct food *f = foods[i];
            char *fIng = (char*)calloc(strlen(f->ingredients), sizeof(char));
            strcpy(fIng, f->ingredients);

            if (inCSV(curr, fIng)) {
                ing->foods[index] = f;
                index++;
            }
        }

        curr = strtok(NULL, ",");
        ingIndex++;
    }

    return;
}

void quickSort(int *arr, int start, int end) {
    if (start >= end) {
        return;
    }

    int pivotIndex = partition(arr, start, end);
    quickSort(arr, start, pivotIndex - 1);
    quickSort(arr, pivotIndex + 1, end);

    return;
}

int partition(int *arr, int start, int end) {
    int pivotValue, pivotIndex = start;
    pivotValue = arr[end];

    for (int i = start; i < end - 1; i++) {
        if (arr[i] > pivotValue) {
            swap(arr, i, pivotIndex);
            pivotIndex++;
        }
    }

    swap(arr, end, pivotIndex);

    return pivotIndex;
}

void swap(int *arr, int a, int b) {
    int temp = arr[a];
    arr[a] = arr[b];
    arr[b] = temp;

    return;
}

char *sortAllergens(char * allergenNames, int numAllergens) {
    char *sorted = (char*)calloc(strlen(allergenNames), sizeof(char)), *unsorted = (char*)calloc(strlen(allergenNames), sizeof(char));
    strcpy(unsorted, allergenNames);
    int index = 0;


    while (strlen(sorted) < strlen(allergenNames)) {
        char *record = unsorted, *temp = unsorted;
        while (temp[0] != ',' && strlen(temp) != 0) {
            temp++;
        }

        char *end = temp;

        while (strlen(temp) != 0) {
            temp++;

            char *tempEnd = temp;
            while (tempEnd[0] != ',' && strlen(tempEnd) != 0) {
                tempEnd++;
            }

            char *t1 = (char*)calloc(end - record + 1, sizeof(char)), *t2 = (char*)calloc(tempEnd - temp + 1, sizeof(char));
            strncpy(t1, record, end - record);
            strncpy(t2, temp, tempEnd - temp);

            if (strcmp(t1, t2) > 0) {
                record = temp;
                end = tempEnd;
            }

            while (temp[0] != ',' && strlen(temp) != 0) {
                temp++;
            }
        }

        if (index != 0) {
            strcat(sorted, ",");
        }

        strncat(sorted, record, end - record);

        char *next = (char*)calloc(strlen(unsorted), sizeof(char)), *p = unsorted;

        while (strlen(p) != 0) {
            if (p < record || p > end) {
                strncat(next, p, 1);
            }
            p++;
        }

        int nextLen = strlen(next);
        if (next[nextLen - 1] == ',') {
            nextLen--;
        }

        unsorted = (char*)calloc(nextLen + 1, sizeof(char));

        strncpy(unsorted, next, nextLen);
        index++;
    }

    return sorted;
}


int main() {
    int numFoods = numLines();
    int *foods = (int*)calloc(numFoods, sizeof(int));
    readData(foods);

    for (int i = 0; i < numFoods; i++) {
        printFood(foods[i]);
    }

    printf("\n\n\n");

    char *allergenNames = findAllergens(foods, numFoods);

    int numAllergens = 1;
    for (int i = 0; i < strlen(allergenNames); i++) {
        if (allergenNames[i] == ',') {
            numAllergens++;
        }
    }

    char *sortedAllergens = sortAllergens(allergenNames, numAllergens);
    strcat(sortedAllergens, ",");

    int *allergens = (int*)calloc(numAllergens, sizeof(int));
    genAllergens(allergenNames, allergens, foods, numAllergens, numFoods);

    for (int i = 0; i < numAllergens; i++) {
        printAllergen(allergens[i]);
    }

    printf("\n\n\n");

    char *ingredientNames = findIngredients(foods, numFoods);

    int numIngredients = 1;
    for (int i = 0; i < strlen(ingredientNames); i++) {
        if (ingredientNames[i] == ',') {
            numIngredients++;
        }
    }

    int *ingredients = (int*)calloc(numIngredients, sizeof(int));
    genIngredients(ingredientNames, ingredients, foods, allergens, numIngredients, numFoods, numAllergens);

    for (int i = 0; i < numIngredients; i++) {
        printIngredient(ingredients[i]);
    }

    printf("\n\n\n");

    for (int i = 0; i < numIngredients; i++) {
        struct ingredient *ing = ingredients[i];
        char *ingName = (char*)calloc(strlen(ing->name), sizeof(char));
        strcpy(ingName, ing->name);

        for (int j = 0; j < numAllergens; j++) {
            if (ing->pAllergen[j] == 0) {
                continue;
            }

            struct allergen *a = ing->pAllergen[j];
            char *allName = (char*)calloc(strlen(a->name), sizeof(char));
            strcpy(allName, a->name);

            bool inAll = true;
            int index = 0;
            while (a->foods[index] != 0) {
                struct food *f = a->foods[index];
                if (!inCSV(ingName, f->ingredients)) {
                    inAll = false;
                    break;
                }

                index++;
            }

            if (!inAll) {
                ing->pAllergen[j] = 0;
            }
        }

        quickSort(ing->pAllergen, 0, 9);
        printIngredient(ing);
    }

    printf("\n\n\n");

    int count = 0;
    for (int i = 0; i < numIngredients; i++) {
        struct ingredient *ing = ingredients[i];
        if (ing->pAllergen[0] == 0) {
            int index = 0;
            while (ing->foods[index] != 0) {
                count++;
                index++;
            }
        }
    }

    printf("Number of instances of ingredients that cannot be allergens: %d\n\n", count);

    bool done;
    do {
        done = true;

        for (int i = 0; i < numAllergens; i++) {
            struct allergen *a = allergens[i];

            for (int j = 0; j < numIngredients; j++) {
                struct ingredient *pos = ingredients[j];

                int index = 0;
                bool found = false;
                while (pos->pAllergen[index] != 0) {
                    if (pos->pAllergen[index] == a) {
                        found = true;
                        break;
                    }

                    index++;
                }

                if (found) {
                    if (a->ing == 0) {
                        a->ing = pos;
                    } else {
                        a->ing = 0;
                        break;
                    }
                }
            }

            if (a->ing == 0) {
                done = false;
            } else {
                struct ingredient *pos = a->ing;
                int index = 0;
                while (pos->pAllergen[index] != 0) {
                    if (pos->pAllergen[index] != a) {
                        pos->pAllergen[index] = 0;
                    }

                    index++;
                }

                quickSort(pos->pAllergen, 0, 9);

                for (int j = 0; j < numIngredients; j++) {
                    if (j == a->ing) {
                        continue;
                    }

                    struct ingredient *pos = ingredients[j];

                    int index = 0;
                    bool found = false;
                    while (pos->pAllergen[index] != 0) {
                        if (pos->pAllergen[index] == a) {
                            found = true;
                            break;
                        }

                        index++;
                    }

                    if (found) {
                        pos->pAllergen[index] = 0;
                        quickSort(pos->pAllergen, 0, 9);
                    }
                }
            }
        }
    } while (!done);

    printf("Cannonical dangerous ingredient list: ");
    char *p = sortedAllergens, *start = p;
    int index = 0;
    while (strlen(p) != 0) {
        if (p[0] == ',') {
            if (index != 0) {
                printf(",");
            }

            char *temp = (char*)calloc(p - start + 1, sizeof(char));

            strncpy(temp, start, p - start);

            for (int i = 0; i < numAllergens; i++) {
                struct allergen *a = allergens[i];

                if (strcmp(a->name, temp) == 0) {
                    struct ingredient *i_ = a->ing;

                    printf("%s", i_->name);
                    break;
                }
            }

            start = p + 1;
            index++;
        }

        p++;
    }

    return 1;
}
