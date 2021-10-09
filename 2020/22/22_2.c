#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#define fileName "input.txt"
#define testFile "input1.txt"
#define dataLine 20
#define test false
#define size 50


typedef struct hand {
    int player, deck[size + 1];
} Hand;

struct hand *createHand(struct hand *h, int p) {
    h->player = p;

    for (int i = 0; i <= size; i++) {
        h->deck[i] = 0;
    }

    return h;
}

void printHand(struct hand *h) {
    printf("Player %d's deck: ", h->player);

    int index = size;
    while (h->deck[index] != 0) {
        if (index != size) {
            printf(", ");
        }

        printf("%d", h->deck[index]);

        index--;
    }

    printf("\n");

    return;
}

void readData(int *players) {
    int player = 0, index = size;
	char textRead[dataLine];
	struct hand *h;

	// Open the file
	FILE *inFile = fopen((test) ? testFile : fileName, "r");

	// Check if the file exists or not
    if (inFile == NULL) {
        return;
    }

	while(fgets(textRead, dataLine, inFile)) {
        if (textRead[0] == 'P') {
            h = players[player];
            player++;
            index = size;
        } else if (textRead[0] != '\n') {
            int num = atoi(textRead);
            h->deck[index] = num;
            index--;
        }
	}

	fclose(inFile);

	return;
}

int popStack(int *arr) {
    int popped;
    for (int i = size; i >= 0; i--) {
        if (i == size) {
            popped = arr[i];
        } else {
            arr[i + 1] = arr[i];
            arr[i] = 0;
        }
    }

    return popped;
}

char *decksToStr(int *players) {
    char *str = (char*)calloc(1, sizeof(char));

    for (int j = 0; j < 2; j++) {
        struct hand *h = players[j];
        char *t = (char*)calloc(10, sizeof(char));
        sprintf(t, "%s: ", (j == 0) ? "A" : "B");
        str = realloc(str, (strlen(str) + strlen(t) + 2) * sizeof(char));
        strcat(str, t);

        for (int i = size; i >= 0 && h->deck[i] != 0; i--) {
            char *temp = (char*)calloc(ceil(log(h->deck[i] + 1)) + 1, sizeof(char));
            sprintf(temp, "%d", h->deck[i]);

            str = realloc(str, (strlen(str) + strlen(temp) + 2) * sizeof(char));

            strcat(str, temp);
            strcat(str, ",");
            free(temp);
        }
    }

    return str;
}

char *inHist(char *pHist, int *players, bool *result) {
    *(result) = false;

    char *curr = decksToStr(players), *tHist = (char*)calloc(strlen(pHist) + 2, sizeof(char)), *p;
    strcpy(tHist, pHist);

    p = strtok(tHist, "A");

    while (p) {
        char *temp = (char*)calloc(strlen(p) + 2, sizeof(char));
        strcat(temp, "A");
        strcat(temp, p);

        if (strncmp(temp, curr, strlen(curr)) == 0) {
            *(result) = true;
            break;
        }

        p = strtok(NULL, "A");
        free(temp);
    }

    char *newHist = (char*)calloc(strlen(pHist) + strlen(curr) + 2, sizeof(char));
    strcpy(newHist, pHist);
    strcat(newHist, curr);

    free(curr), free(tHist), free(pHist);

    return newHist;
}


int newGame(int *players, int *game, int layer) {
    int round = 1, thisGame = *(game);
    char *hist = (char*)calloc(1, sizeof(char));

    printf("=== Game %d ===\n\n", thisGame);

    while (true) {
        int num[2];

        printf("-- Round %d (Game %d, Layer %d) --\n", round, thisGame, layer);
        for (int i = 0; i < 2; i++) {
            printHand(players[i]);
        }

        bool found;
        hist = inHist(hist, players, &found);

        if (found) {
            printf("Cards are in a previous state!\nPlayer 1 wins game %d!\n\n", thisGame);

            free(hist);
            return 0;
        }

        for (int i = 0; i < 2; i++) {
            struct hand *h = players[i];
            num[i] = popStack(h->deck);
            printf("Player %d plays: %d\n", i + 1, num[i]);
        }

        int *cards = (int*)calloc(2, sizeof(int));
        for (int i = 0; i < 2; i++) {
            struct hand *h = players[i];

            for (int j = 0; j <= size; j++) {
                cards[i] += h->deck[j] != 0 ? 1 : 0;
            }
        }

        int winner;
        if (cards[0] >= num[0] && cards[1] >= num[1]) {
            // Recursion
            printf("Playing a sub-game to determine the winner...\n\n");

            int *newPlayers = (int*)calloc(2, sizeof(int));
            for (int i = 0; i < 2; i++) {
                struct hand *h = (struct hand*)calloc(1, sizeof(struct hand));
                h = createHand(h, i + 1);
                newPlayers[i] = h;
            }

            for (int i = 0; i < 2; i++) {
                struct hand *oldH = players[i], *newH = newPlayers[i];

                for (int j = size; j > size - num[i] && j >= 0; j--) {
                    newH->deck[j] = oldH->deck[j];
                }
            }

            *(game) = *(game) + 1;

            winner = newGame(newPlayers, game, layer + 1);

            free(newPlayers);
            printf("...anyway, back to game %d.\n", thisGame);
        } else {
            // Standard
            winner = (num[0] > num[1]) ? 0 : 1;
        }

        struct hand *h = players[winner];

        int index = 0;
        while (h->deck[index] == 0) {
            index++;
        }

        index--;

        h->deck[index] = num[winner];
        h->deck[index - 1] = num[(winner + 1) % 2];

        printf("Player %d wins round %d of game %d!\n\n", winner + 1, round, thisGame);

        round++;

        for (int i = 0; i < 2; i++) {
            struct hand *h = players[i];
            if (h->deck[size] == 0) {
                int winner = (i + 1) % 2;
                printf("Player %d wins game %d!\n\n", winner + 1, thisGame);

                free(hist);
                return winner;
            }
        }
    }
}


int main() {
    int players[2];
    for (int i = 1; i <= 2; i++) {
        struct hand *h = (struct hand*)calloc(1, sizeof(struct hand));
        h = createHand(h, i);
        players[i - 1] = h;
    }

    readData(&players[0]);

    int game = 1, winner = newGame(&players[0], &game, 1);


    printf("\n\nGAME OVER! Player %d wins!\n\n", winner + 1);

    int count = 0;
    printf("Final hands:\n");
    for (int i = 0; i < 2; i++) {
        struct hand *h = players[i];
        printHand(h);

        int mult = 1;

        for (int j = 0; j <= size; j++) {
            if (h->deck[j] != 0) {
                count += mult * h->deck[j];
                mult++;
            }
        }
    }

    printf("\nWinners score: %d\n", count);

    return 1;
}
