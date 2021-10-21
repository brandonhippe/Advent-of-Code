#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
//#define test

int findLoopSize(int pk) {
    int count = 0, value = 1, subject = 7;

    while (value != pk) {
        value *= subject;
        value = value % 20201227;
        count++;
    }

    return count;
}

int main() {
    int cardLoop = 0, doorLoop = 0, cardPk, doorPk;

    #ifdef test
        cardPk = 5764801;
        doorPk = 17807724;
    #endif // test
    #ifndef test
        cardPk = 1327981;
        doorPk = 2822615;
    #endif // test

    cardLoop = findLoopSize(cardPk);
    doorLoop = findLoopSize(doorPk);

    int loop = (cardLoop < doorLoop) ? cardLoop : doorLoop, subject = (cardLoop < doorLoop) ? doorPk : cardPk;

    unsigned long long int sk = 1;
    for (int i = 0; i < loop; i++) {
        sk *= subject;
        sk = sk % 20201227;
    }

    printf("The encryption key is: %llu\n", sk);

    return 1;
}
