#ifndef SET_H
#define SET_H


// Include headers
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "vector.h"
#include "adts.h"


// Function Prototypes
struct set *createSet(size_t (*size)(void *e), void *(*copy)(void *e, size_t size));
void deleteSet(struct set *s, bool delEls);
int setHash(void *e, size_t size);
void addSet(struct set *s, void *e);
void removeSet(struct set *s, void *e);
struct set *setIntersection(struct set *s1, struct set *s2);
struct set *setUnion(struct set *s1, struct set *s2);
bool inSet(struct set *s, void *e);
void *createCopySet(void *z, size_t setSize);
size_t sizeofSet(void *s);
struct vector *set2vector(struct set *s);
struct set *vector2set(struct vector *v);


// Declare Set Struct
struct set {
    int len, cap, hashMult;
    double avgHash, loadMax;
    size_t (*e_size)(void *e);  // Function to calculate size of an element
    void *(*e_cpy)(void *e, size_t size);   // Function to create a copy of an element
    int (*hashFunc)(void *key, size_t size); // Function to calculate hash of an element
    struct vector *setVector;
};


// Function to create a set
struct set *createSet(size_t (*size)(void *e), void *(*copy)(void *e, size_t size)) {
    struct set *s = (struct set *)malloc(sizeof(struct set));
    s->len = 0;
    s->cap = 1;
    s->hashMult = 1;
    s->avgHash = 0;
    s->loadMax = 0.75;
    s->e_size = size;
    s->e_cpy = copy;
    s->hashFunc = setHash;
    s->setVector = createVector(sizeofVector, createCopyVector);
    appendVector(s->setVector, (void*)createVector(size, copy));

    return s;
}


// Function to delete a set
void deleteSet(struct set *s, bool delEls) {
    deleteVector(s->setVector, delEls);
    free(s);
}


// Calculate an element's hash
int setHash(void *e, size_t size) {
    char *e_str = (char*)e;

    int hash = 1;

    for (int i = 0; i < size; i++) {
        hash += e_str[i] - CHAR_MIN;
    }

    return hash;
}


// Add an element to a set
void addSet(struct set *s, void *e) {
    if (inSet(s, e)) {
        return;
    }

    int hash = s->hashFunc(e, s->e_size(e)) * s->hashMult;
    s->avgHash = s->avgHash * (s->len / (double)(s->len + 1)) + (hash / (double)(s->len + 1));
    hash %= s->cap;

    struct vector *bucket = s->setVector->arr[hash];
    appendVector(bucket, e);

    s->len++;

    while ((double)s->len / (double)s->cap > s->loadMax) {
        s->cap *= 2;

        s->avgHash /= s->hashMult;
        s->hashMult = 1;

        while (s->cap > s->avgHash * s->hashMult) {
            s->hashMult += 2;
        }

        s->avgHash *= s->hashMult;

        struct vector *newSetVector = createVectorSized(sizeofVector, createCopyVector, s->cap);
        for (int i = 0; i < s->cap; i++) {
            appendVector(newSetVector, createVector(s->e_size, s->e_cpy));
        }

        for (int i = 0; i < s->setVector->len; i++) {
            struct vector *b = s->setVector->arr[i];
            for (int j = 0; j < b->len; j++) {
                hash = (s->hashFunc(b->arr[j], s->e_size(b->arr[j])) * s->hashMult) % s->cap;
                bucket = newSetVector->arr[hash];
                appendVector(bucket, b->arr[j]);
            }
        }

        deleteVector(s->setVector, false);
        s->setVector = newSetVector;
    }
}


// Remove an element from a set
void removeSet(struct set *s, void *e){
    if (!inSet(s, e)) {
        return;
    }

    int hash = s->hashFunc(e, s->e_size(e)) * s->hashMult;
    hash %= s->cap;
    
    if (s->len > 1) {
        s->avgHash = s->avgHash * (s->len / (s->len - 1)) - (hash / (s->len - 1));
    } else {
        s->avgHash = 0;
    }

    struct vector *bucket = s->setVector->arr[hash];
    int ix = indexVector(bucket, e, s->e_size(e));
    bucket->arr[ix] = popVector(bucket);

    s->len--;


    while (s->len > 0 && s->cap > 1 && (double)s->len / (double)s->cap < s->loadMax / 4.0) {
        s->cap /= 2;

        s->avgHash /= s->hashMult;
        s->hashMult = 1;

        while (s->cap > s->avgHash * s->hashMult) {
            s->hashMult += 2;
        }

        s->avgHash *= s->hashMult;

        struct vector *newSetVector = createVectorSized(s->e_size, s->e_cpy, s->cap);
        for (int i = 0; i < s->cap; i++) {
            appendVector(newSetVector, (void*)createVector(s->e_size, s->e_cpy));
        }

        for (int i = 0; i < s->setVector->len; i++) {
            struct vector *b = s->setVector->arr[i];
            for (int j = 0; j < b->len; j++) {
                hash = (s->hashFunc(b->arr[j], s->e_size(b->arr[j])) * s->hashMult) % s->cap;
                bucket = newSetVector->arr[hash];
                appendVector(bucket, b->arr[j]);
            }
        }

        deleteVector(s->setVector, false);
        s->setVector = newSetVector;
    }
}


// Determine Intersection of two sets
struct set *setIntersection(struct set *s1, struct set *s2){
    if (s1->e_cpy == s2->e_cpy && s1->e_size == s2->e_size) {
        struct set *intersect = createSet(s1->e_size, s1->e_cpy);
        struct vector *v1 = set2vector(s1);

        for (int i = 0; i < v1->len; i++) {
            if (inSet(s2, v1->arr[i])) {
                addSet(intersect, v1->arr[i]);
            }
        }

        return intersect;
    } else {
        exit(-1);
    }
}


// Determine Union of two sets
struct set *setUnion(struct set *s1, struct set *s2) {
    if (s1->e_cpy == s2->e_cpy && s1->e_size == s2->e_size) {
        struct set *un = createSet(s1->e_size, s1->e_cpy);
        struct vector *v1 = set2vector(s1), *v2 = set2vector(s2);

        for (int i = 0; i < v1->len; i++) {
            addSet(un, v1->arr[i]);
        }

        for (int i = 0; i < v2->len; i++) {
            addSet(un, v2->arr[i]);
        }

        return un;
    } else {
        exit(-1);
    }
}


// Determine if an element is in a set
bool inSet(struct set *s, void *e) {
    size_t size = s->e_size(e);
    int hash = (s->hashFunc(e, size) * s->hashMult) % s->cap;
    struct vector *bucket = s->setVector->arr[hash];
    return inVector(bucket, e, size);
}


// Creates a copy of set
void *createCopySet(void *z, size_t setSize) {
    struct set *s = (struct set*)z;
    struct set *newS = createSet(s->e_size, s->e_cpy);

    newS->len = s->len;
    newS->cap = s->cap;
    newS->hashMult = s->hashMult;
    newS->avgHash = s->avgHash;
    newS->loadMax = s->loadMax;
    newS->setVector = createCopyVector(s->setVector, sizeof(struct vector));

    return newS;
}


// Get size of set type
size_t sizeofSet(void *s) {
    return sizeof(struct set);
}


// Convert a set into a vector
struct vector *set2vector(struct set *s) {
    struct vector *v = createVector(s->e_size, s->e_cpy);

    for (int i = 0; i < s->setVector->len; i++) {
        struct vector *bucket = createCopyVector(s->setVector->arr[i], sizeof(struct vector));
        for (int j = 0; j < bucket->len; j++) {
            appendVector(v, bucket->arr[j]);
        } 
    }

    return v;
}


// Convert a vector into a set
struct set *vector2set(struct vector *v) {
    struct set *s = createSet(v->e_size, v->e_cpy);
    struct vector *vec = createCopyVector(v, sizeof(struct vector));

    for (int i = 0; i < vec->len; i++) {
        addSet(s, vec->arr[i]);
    }

    return s;
}


#endif