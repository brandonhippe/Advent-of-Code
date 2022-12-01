#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#include "C:\Users\Brandon Hippe\Documents\Coding Projects\Advent-of-Code\Modules\input.h"
#define fileName "input.txt"


char *hex2bin(char c) {
    long n = strtol(&c, NULL, 16);
    char *b = (char*)calloc(4, sizeof(char));

    for (int i = 0; i < 4; i++) {
        strcat(b, n % 2 == 0 ? "0" : "1");
        n /= 2;
    }

    b = strrev(b);
    return b;
}


int bin2int(char *b) {
    int n = 0;

    for (int i = 0; i < strlen(b); i++) {
        n *= 2;
        n += b[i] == '1' ? 1 : 0;
    }

    return n;
}


char *packetEval(char *packet, int *vSum, int *packetBits, long long int *val) {
    int type = 0, lengthType = 0, subPacketNum = 0, subPacketBits = 0;

    int i = 0, numBits;

    bool continuing = true;

    while (continuing) {
        if (i == 0 || i == 3) {
            numBits = 3;
        } else if (i == 6 && type != 4) {
            numBits = 1;
        } else if (i >= 6 && type == 4) {
            numBits = 5;
        } else if (i == 7) {
            if (lengthType == 0) {
                numBits = 15;
            } else {
                numBits = 11;
            }
        }

        *packetBits = *packetBits + numBits;

        char *selectedBits = (char*)calloc(numBits + 1, sizeof(char));
        strncpy(selectedBits, packet, numBits);

        if (i == 0) {
            *vSum = *vSum + bin2int(selectedBits);
        } else if (i == 3) {
            type = bin2int(selectedBits);
        } else if (type == 4) {
            continuing = packet[0] == '1';
            *val = *val * 16;
            *val = *val + bin2int(selectedBits + 1);
        } else if (i == 6) {
            lengthType = packet[0] == '1' ? 1 : 0;
        } else {
            packet += numBits;

            if (lengthType == 0) {
                subPacketBits = bin2int(selectedBits);
            } else {
                subPacketNum = bin2int(selectedBits);
            }

            int sPbits = 0, sPnum = 0;
            long long int *vals = (long long int*)calloc(1, sizeof(long long int));
            while ((lengthType == 0 && sPbits < subPacketBits) || (lengthType == 1 && sPnum < subPacketNum)) {
                if (sPnum != 0) {
                    vals = (long long int*)realloc(vals, sizeof(long long int) * (sPnum + 1));
                    vals[sPnum] = 0;
                }

                packet = packetEval(packet, vSum, &sPbits, &vals[sPnum]);
                sPnum += 1;
            }

            *packetBits = *packetBits + sPbits;
            switch (type) {
            case 0:
                *val = 0;
                for (int i = 0; i < sPnum; i++) {
                    *val = *val + vals[i];
                }
                break;

            case 1:
                *val = 1;
                for (int i = 0; i < sPnum; i++) {
                    *val = *val * vals[i];
                }
                break;
            
            case 2:
                *val = vals[0];
                for (int i = 1; i < sPnum; i++) {
                    *val = vals[i] < *val ? vals[i] : *val;
                }
                break;

            case 3:
                *val = vals[0];
                for (int i = 1; i < sPnum; i++) {
                    *val = vals[i] > *val ? vals[i] : *val;
                }
                break;

            case 5:
                *val = vals[0] > vals[1];
                break;

            case 6:
                *val = vals[0] < vals[1];
                break;

            case 7:
                *val = vals[0] == vals[1];
                break;
            }

            break;
        }

        i += numBits;
        packet += numBits;
    }

    return packet;
}


int main () {
    struct vector *input_data = singleLine(fileName, " ");
    char *data = (char*)input_data->arr[0];
    char *bits = (char*)calloc(strlen(data) * 4 + 1, sizeof(char));
    for (int i = 0; i < strlen(data); i++) {
        strcat(bits, hex2bin(data[i]));
    }

    int *vSum = (int*)calloc(1, sizeof(int)), *packetBits = (int*)calloc(1, sizeof(int));
    long long int *packetValue = (long long int*)calloc(1, sizeof(long long int));
    packetEval(bits, vSum, packetBits, packetValue);

    printf("\nPart 1:\nSum of version numbers: %d\n", *vSum);
    printf("\nPart 2:\nPacket Value: %lld\n", *packetValue);

    return 1;
}
