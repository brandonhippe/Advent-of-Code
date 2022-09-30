#ifndef HEAPQ_H
#define HEAPQ_H


// Include header files
#include <stdlib.h>
#include <stdio.h>
#include "vector.h"


// Declare heap struct
struct heap {
    struct vector *heapVec;
    bool (*cmp)(void *e1, void *e2);
};


// Function Prototypes
struct heap *createHeap(struct vector *hVec, bool (*cmp)(void *e1, void *e2));
void appendHeap(struct heap *h, void *e);


// Create a heap struct
struct heap *createHeap(struct vector *hVec, bool (*cmp)(void *e1, void *e2)) {
    struct heap *h = (struct heap*)calloc(1, sizeof(struct heap));
    h->heapVec = hVec;
    h->cmp = cmp;

    return h;
}


// Add to a heap
void appendHeap(struct heap *h, void *e) {
    appendVector(h->heapVec, e);

    int ix = h->heapVec->len - 1;
    while (ix > 0 && h->cmp(e, h->heapVec->arr[ix / 2])) {
        h->heapVec->arr[ix] = h->heapVec->arr[ix / 2];
        ix /= 2;
        h->heapVec->arr[ix] = e;
    }
}


// Remove minimum element from a heap
void *popHeap(struct heap *h) {
    void *popped = h->heapVec->arr[0];
    h->heapVec->arr[0] = h->heapVec->arr[h->heapVec->len - 1];
    popVector(h->heapVec);

    int ix = 0;
    while (true) {
        int nIx = (h->cmp(h->heapVec->arr[2 * ix + 1], h->heapVec->arr[2 * ix + 2])) ? 2 * ix + 1 : 2 * ix + 2;

        if (h->cmp(h->heapVec->arr[ix], h->heapVec->arr[nIx])) {
            break;
        }

        void *temp = h->heapVec->arr[ix];
        h->heapVec->arr[ix] = h->heapVec->arr[nIx];
        h->heapVec->arr[nIx] = temp;

        ix = nIx;
    }

    return popped;
}


#endif