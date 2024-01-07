#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#define data 326519478
//#define test 389125467

const int maxMoves = 10000000;

typedef struct cup {
    int val;
    struct cup *next;
} Cup;

struct cup *createCup(struct cup *c, int num) {
    c->val = num;

    return c;
}

void printCup(struct cup *c) {
    printf("Cup #%d. Ptr 0x%x (%d), Next ptr: 0x%x (%d)\n", c->val, c, c, c->next, c->next);

    return;
}

void printCups(struct cup *start) {
    struct cup *print = start;

    do {
        printf("%d", print->val);
        print = print->next;
    } while (print != start);

    printf("\n");

    return;
}

int main() {
    char order[10];
    int moves = maxMoves, *ptrs = (int*)calloc(1000000, sizeof(int));

    #ifdef test
        sprintf(order, "%d", test);
    #endif // test

    #ifndef test
        sprintf(order, "%d", data);
    #endif // test

    struct cup *past = NULL, *start;
    char *index = &order;

    while (strlen(index) > 0) {
        struct cup *c = (struct cup*)calloc(1, sizeof(struct cup));
        c = createCup(c, index[0] - 48);

        ptrs[index[0] - 49] = c;

        if (past) {
            past->next = c;
        } else {
            start = c;
        }

        past = c;
        index++;
    }

    for (int i = 10; i <= 1000000; i++) {
        struct cup *c = (struct cup*)calloc(1, sizeof(struct cup));
        c = createCup(c, i);

        ptrs[i - 1] = c;

        past->next = c;
        past = c;
    }

    past->next = start;

    int percent = 1;

    while (moves > 0) {
        if ((moves % 100000)  == 0) {
            printf("%d%%\n", percent);
            percent++;
        }

        int pickup[3], pickupVals[3];

        struct cup *t = start->next;
        for (int i = 0; i < 3; i++) {
            pickup[i] = t;
            pickupVals[i] = t->val;
            t = t->next;
        }

        int dest = start->val;
        bool inPickup;

        do {
            inPickup = false;

            if (dest == 1) {
                dest = 1000001;
            }

            dest--;
            for (int i = 0; i < 3; i++) {
                if (pickupVals[i] == dest) {
                    inPickup = true;
                    break;
                }
            }
        } while (inPickup);

        struct cup *destCup = ptrs[dest - 1], *endPickup = pickup[2];
        start->next = endPickup->next;
        endPickup->next = destCup->next;
        destCup->next = pickup[0];

        start = start->next;
        moves--;
    }
	
	printf("\n");
    start = ptrs[0];

    unsigned long long int product = 1;
    for (int i = 0; i < 2; i++) {
        start = start->next;
        printf("%d\n", start->val);
        product *= start->val;
    }

    printf("Product of two cups immediately next to cup 1: %llu\n", product);

    return 1;
}
