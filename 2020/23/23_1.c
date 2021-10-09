#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#define data 326519478
//#define test 389125467

const int maxMoves 100
//const int maxMoves 10

typedef struct cup {
    int val;
    struct cup *next;
} Cup;

struct cup *createCup(struct cup *c, char num) {
    c->val = num - 48;

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
    int moves = maxMoves;
	
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
        c = createCup(c, index[0]);

        if (past) {
            past->next = c;
        } else {
            start = c;
        }

        past = c;
        index++;
    }

    past->next = start;

    struct cup *print = start;
    do {
        printCup(print);
        print = print->next;
    } while (print != start);

    printf("\n\n");


    while (moves > 0) {
        printf("-- Move %d --\nCups: ", maxMoves - moves + 1);
        printCups(start);

        int pickup[3], pickupVals[3];

        printf("Pick up: ");

        struct cup *t = start->next;
        for (int i = 0; i < 3; i++) {
            pickup[i] = t;
            pickupVals[i] = t->val;
            printf("%d", t->val);
            t = t->next;
        }

        int dest = start->val;
        bool inPickup;

        do {
            inPickup = false;

            if (dest == 1) {
                dest = 10;
            }

            dest--;
            for (int i = 0; i < 3; i++) {
                if (pickupVals[i] == dest) {
                    inPickup = true;
                    break;
                }
            }
        } while (inPickup);

        printf("\nDestination: %d\n\n", dest);

        struct cup *destCup = start;
        while (destCup->val != dest) {
            destCup = destCup->next;
        }

        struct cup *endPickup = pickup[2];
        start->next = endPickup->next;
        endPickup->next = destCup->next;
        destCup->next = pickup[0];

        start = start->next;
        moves--;
    }

    while (start->val != 1) {
        start = start->next;
    }

    printf("-- Final --\nCups:");
    printCups(start);


    return 1;
}
