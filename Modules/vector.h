#ifndef VECTOR_H
#define VECTOR_H


// Include headers
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "adts.h"


// Function Prototypes
struct vector *createVector(size_t (*size)(void *e), void *(*copy)(void *e, size_t size));
struct vector *createVectorSized(size_t (*size)(void *e), void *(*copy)(void *e, size_t size), int numEls);
void deleteVector(struct vector *v, bool delEls);
void appendVector(struct vector *v, void *e);
void* popVector(struct vector *v);
struct vector *sliceVector(struct vector *v, int start, int end, int step);
bool inVector(struct vector *v, void *e, size_t size);
int indexVector(struct vector *v, void *e, size_t size);
void *createCopyVector(void *vec, size_t vecSize);
size_t sizeofVector(void *e);
struct vector *sortVector(struct vector *v, bool (*cmp)(void *e1, void *e2));


// Declare Vector Struct
struct vector {
    int len, cap;
    size_t (*e_size)(void *e);  // Function to calculate size of an element
    void *(*e_cpy)(void *e, size_t size);   // Function to create a copy of an element
    void **arr;
};


// Function to create a vector
struct vector *createVector(size_t (*size)(void *e), void *(*copy)(void *e, size_t size)) {
    struct vector *v = (struct vector *)malloc(sizeof(struct vector));
    v->len = 0, v->cap = 1;
    v->e_size = size;
    v->e_cpy = copy;
    v->arr = (void**)calloc(1, sizeof(void*));

    return v;
}


// Function to create vector of a certain size
struct vector *createVectorSized(size_t (*size)(void *e), void *(*copy)(void *e, size_t size), int numEls) {
    if (numEls > 0) {
        struct vector *v = (struct vector *)malloc(sizeof(struct vector));
        v->len = 0, v->cap = numEls;
        v->e_size = size;
        v->e_cpy = copy;
        v->arr = (void**)calloc(numEls, sizeof(void*));

        return v;
    } else {
        return NULL;
    }
}


// Function to delete a vector
void deleteVector(struct vector *v, bool delEls) {
    if (delEls) {
        for (int i = 0; i < v->len; i++) {
            free(v->arr[i]);
        }
    }
    free(v->arr);
    free(v);
}


// Function to append an element to a vector
void appendVector(struct vector *v, void *e) {
    if (v->len == v->cap) {
        void **newArr = (void**)calloc(2 * v->cap, sizeof(void*));
        
        for (int i = 0; i < v->len; i++) {
            newArr[i] = v->arr[i];
        }

        free(v->arr);
        v->arr = newArr;
        v->cap *= 2;
    }

    v->arr[v->len] = e;
    v->len++;
}


// Function to pop last element from a vector
void* popVector(struct vector *v) {
    void *e = v->arr[v->len - 1];
    v->arr[v->len - 1] = NULL;
    v->len--;

    if (v->cap > 1 && v->len <= v->cap / 4) {
        void **newarr = (void**)calloc(v->cap / 2, sizeof(void*));

        for (int i = 0; i < v->len; i++) {
            newarr[i] = v->arr[i];
        }

        free(v->arr);
        v->arr = newarr;
        v->cap /= 2;
    }

    return e;
}


// Function to create a slice of a vector. Copies elements based on deepcopy
struct vector *sliceVector(struct vector *v, int start, int end, int step) {
    if ((start < 0 || start > v->len) || (end < 0 || end > v->len) || step == 0) {
        return NULL;
    }

    struct vector *sliced = createVector(v->e_size, *v->e_cpy);

    for (int i = start; (i < end && step > 0) || (i > end && step < 0); i += step) {
        appendVector(sliced, v->arr[i]);
    }

    return sliced;
}


// Function to determine if an element is in a vector
bool inVector(struct vector *v, void *e, size_t size) {
    for (int i = 0; i < v->len; i++) {
        if (v->e_size(v->arr[i]) == size && strncmp((char*)e, (char*)v->arr[i], size) == 0) {
            return true;
        }
    }
    
    return false;
}


// Function to get index of an element if it is in the vector
int indexVector(struct vector *v, void *e, size_t size) {
    for (int i = 0; i < v->len; i++) {
        char *str = (char*)v->e_cpy(v->arr[i], v->e_size(v->arr[i]));
        if (v->e_size(v->arr[i]) == size && strncmp((char*)e, str, size) == 0) {
            return i;
        }
    }
    
    return -1;
}


// Creates a copy of vector
void *createCopyVector(void *vec, size_t vecSize) {
    struct vector *v = (struct vector *)vec;
    struct vector *copy = createVector(v->e_size, *v->e_cpy);

    for (int i = 0; i < v->len; i++) {
        void *newE = v->e_cpy(v->arr[i], v->e_size(v->arr[i]));
        appendVector(copy, newE);
    }

    return copy;
}


// Get size of vector type
size_t sizeofVector(void *e) {
    return sizeof(struct vector);
}


// Merge sorted vectors
struct vector *mergeVec(struct vector *v1, struct vector *v2, bool (*cmp)(void *e1, void *e2)) {
    struct vector *merged = createVector(v1->e_size, v1->e_cpy);
    int i1 = 0, i2 = 0;
    
    while (i1 < v1->len && i2 < v2->len) {
        void *e;
        if (cmp(v1->arr[i1], v2->arr[i2])) {
            e = v1->arr[i1];
            i1++;
        } else {
            e = v2->arr[i2];
            i2++;
        }

        appendVector(merged, e);
    }

    for (int i = i1; i < v1->len; i++) {
        appendVector(merged, v1->arr[i]);
    }

    for (int i = i2; i < v2->len; i++) {
        appendVector(merged, v2->arr[i]);
    }

    return merged;
}


// Sort a vector
struct vector *sortVector(struct vector *v, bool (*cmp)(void *e1, void *e2)) {
    if (v->len == 1) {
        return v;
    }

    return mergeVec(sortVector(sliceVector(v, 0, v->len / 2, 1), cmp), sortVector(sliceVector(v, v->len / 2, v->len, 1), cmp), cmp);
}


#endif