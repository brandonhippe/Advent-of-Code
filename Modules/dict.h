#ifndef DICT_H
#define DICT_H


// Include headers
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include "vector.h"
#include "adts.h"


// Function Prototypes
struct dict *createDict(size_t (*ksize)(void *k), size_t (*vsize)(void *v), void *(*copy)(void *e, size_t size));
void deleteDict(struct dict *d, bool delKeys, bool delVals);
int dictHash(void *key, size_t size);
void addDict(struct dict *d, void *key, void *val);
void removeDict(struct dict *d, void *key);
bool inDict(struct dict *d, void *key);
void *getDictVal(struct dict *d, void *key);
void *createCopyDict(void *z, size_t dictSize);
size_t sizeofDict(void *d);
struct vector *keys2vector(struct dict *d);
struct vector *values2vector(struct dict *d);
struct dict *vector2dict(struct vector *keys, struct vector *values);


// Declare Dict Struct
struct dict {
    int len, cap, hashMult;
    double avgHash, loadMax;
    size_t (*key_size)(void *key), (*val_size)(void *val);  // Function to calculate size of a key/val
    void *(*e_cpy)(void *e, size_t size);   // Function to create a copy of an element
    int (*hashFunc)(void *key, size_t size); // Function to calculate hash of an element
    struct vector *keyVector, *valVector;
};


// Function to create a dict
struct dict *createDict(size_t (*ksize)(void *k), size_t (*vsize)(void *v), void *(*copy)(void *e, size_t size)) {
    struct dict *d = (struct dict *)malloc(sizeof(struct dict));
    d->len = 0;
    d->cap = 1;
    d->hashMult = 1;
    d->avgHash = 0;
    d->loadMax = 0.75;
    d->key_size = ksize;
    d->val_size = vsize;
    d->e_cpy = copy;
    d->hashFunc = dictHash;
    d->keyVector = createVector(sizeofVector, createCopyVector);
    d->valVector = createVector(sizeofVector, createCopyVector);
    appendVector(d->keyVector, createVector(ksize, copyElement));
    appendVector(d->valVector, createVector(vsize, copy));

    return d;
}


// Function to delete a dict
void deleteDict(struct dict *d, bool delKeys, bool delVals) {
    deleteVector(d->keyVector, delKeys);
    deleteVector(d->valVector, delVals);
    free(d);
}


// Calculate an element's hash
int dictHash(void *key, size_t size) {
    char *key_str = (char*)key;

    int hash = 1;

    for (int i = 0; i < size; i++) {
        hash += key_str[i] - CHAR_MIN;
    }

    return hash;
}


// Add an element to a dict
void addDict(struct dict *d, void *key, void *val) {
    if (inDict(d, key)) {
        return;
    }
    
    int hash = d->hashFunc(key, d->key_size(key)) * d->hashMult;
    d->avgHash = d->avgHash * (d->len / (double)(d->len + 1)) + (hash / (double)(d->len + 1));
    hash %= d->cap;

    struct vector *kbucket = d->keyVector->arr[hash], *vbucket = d->valVector->arr[hash];
    appendVector(kbucket, key);
    appendVector(vbucket, val);

    d->len++;

    while ((double)d->len / (double)d->cap > d->loadMax) {
        d->cap *= 2;

        d->avgHash /= d->hashMult;
        d->hashMult = 1;

        while (d->cap > d->avgHash * d->hashMult) {
            d->hashMult += 2;
        }

        d->avgHash *= d->hashMult;

        struct vector *newKeyVector = createVectorSized(sizeofVector, createCopyVector, d->cap);
        struct vector *newValVector = createVectorSized(sizeofVector, createCopyVector, d->cap);
        for (int i = 0; i < d->cap; i++) {
            appendVector(newKeyVector, createVector(d->key_size, copyElement));
            appendVector(newValVector, createVector(d->val_size, d->e_cpy));
        }

        for (int i = 0; i < d->keyVector->len; i++) {
            struct vector *kb = d->keyVector->arr[i];
            struct vector *vb = d->valVector->arr[i];
            for (int j = 0; j < kb->len; j++) {
                hash = (d->hashFunc(kb->arr[j], d->key_size(kb->arr[j])) * d->hashMult) % d->cap;
                kbucket = newKeyVector->arr[hash];
                vbucket = newValVector->arr[hash];
                appendVector(kbucket, kb->arr[j]);
                appendVector(vbucket, vb->arr[j]);
            }
        }

        deleteVector(d->keyVector, false);
        deleteVector(d->valVector, false);
        d->keyVector = newKeyVector;
        d->valVector = newValVector;
    }
}


// Remove an element from a dict
void removeDict(struct dict *d, void *key) {
    if (!inDict(d, key)) {
        return;
    }

    int hash = d->hashFunc(key, d->key_size(key)) * d->hashMult;
    hash %= d->cap;
    
    if (d->len > 1) {
        d->avgHash = d->avgHash * (d->len / (d->len - 1)) - (hash / (d->len - 1));
    } else {
        d->avgHash = 0;
    }

    struct vector *kbucket = d->keyVector->arr[hash], *vbucket = d->valVector->arr[hash];
    int ix = indexVector(kbucket, key, d->key_size(key));
    kbucket->arr[ix] = popVector(kbucket);
    vbucket->arr[ix] = popVector(vbucket);

    d->len--;

    while (d->len > 0 && d->cap > 1 && (double)d->len / (double)d->cap < d->loadMax / 0.4) {
        d->cap /= 2;

        d->avgHash /= d->hashMult;
        d->hashMult = 1;

        while (d->cap > d->avgHash * d->hashMult) {
            d->hashMult += 2;
        }

        d->avgHash *= d->hashMult;

        struct vector *newKeyVector = createVectorSized(sizeofVector, createCopyVector, d->cap);
        struct vector *newValVector = createVectorSized(sizeofVector, createCopyVector, d->cap);
        for (int i = 0; i < d->cap; i++) {
            appendVector(newKeyVector, createVector(d->key_size, copyElement));
            appendVector(newValVector, createVector(d->val_size, d->e_cpy));
        }

        for (int i = 0; i < d->keyVector->len; i++) {
            struct vector *kb = d->keyVector->arr[i];
            struct vector *vb = d->valVector->arr[i];
            for (int j = 0; j < kb->len; j++) {
                hash = (d->hashFunc(kb->arr[j], d->key_size(kb->arr[j])) * d->hashMult) % d->cap;
                kbucket = newKeyVector->arr[hash];
                vbucket = newValVector->arr[hash];
                appendVector(kbucket, kb->arr[j]);
                appendVector(vbucket, vb->arr[j]);
            }
        }

        deleteVector(d->keyVector, false);
        deleteVector(d->valVector, false);
        d->keyVector = newKeyVector;
        d->valVector = newValVector;
    }
}


// Determine if an element is in a dict
bool inDict(struct dict *d, void *key) {
    int hash = (d->hashFunc(key, d->key_size(key)) * d->hashMult) % d->cap;
    struct vector *bucket = d->keyVector->arr[hash];
    return inVector(bucket, key, d->key_size(key));
}


void *getDictVal(struct dict *d, void *key) {
    if (!inDict(d, key)) {
        return NULL;
    }

    int hash = (d->hashFunc(key, d->key_size(key)) * d->hashMult) % d->cap;
    struct vector *kbucket = d->keyVector->arr[hash], *vbucket = d->valVector->arr[hash];
    return vbucket->arr[indexVector(kbucket, key, d->key_size(key))];
}


// Creates a copy of dict
void *createCopyDict(void *z, size_t dictSize) {
    struct dict *d = (struct dict*)z;
    struct dict *newD = createDict(d->key_size, d->val_size, d->e_cpy);

    newD->len = d->len;
    newD->cap = d->cap;
    newD->hashMult = d->hashMult;
    newD->avgHash = d->avgHash;
    newD->loadMax = d->loadMax;
    newD->keyVector = createCopyVector(d->keyVector, sizeof(struct vector));
    newD->valVector = createCopyVector(d->valVector, sizeof(struct vector));

    return newD;
}


// Get size of dict type
size_t sizeofDict(void *d) {
    return sizeof(struct dict);
}


// Turn keys of dict into vector
struct vector *keys2vector(struct dict *d) {
    struct vector *kvector = createVector(d->key_size, copyElement);
    for (int i = 0; i < d->keyVector->len; i++) {
        struct vector *bucket = d->keyVector->arr[i];
        for (int j = 0; j < bucket->len; j++) {
            appendVector(kvector, bucket->arr[j]);
        }
    }

    return kvector;
}


// Turn values of dict into vector
struct vector *values2vector(struct dict *d) {
    struct vector *vvector = createVector(d->val_size, copyElement);
    for (int i = 0; i < d->valVector->len; i++) {
        struct vector *bucket = d->valVector->arr[i];
        for (int j = 0; j < bucket->len; j++) {
            appendVector(vvector, bucket->arr[j]);
        }
    }

    return vvector;
}


// Turn vector of keys and vector of values into dict
struct dict *vector2dict(struct vector *keys, struct vector *values) {
    if (keys->len != values->len) {
        return NULL;
    }

    struct dict *d = createDict(keys->e_size, values->e_size, values->e_cpy);
    for (int i = 0; i < keys->len; i++) {
        addDict(d, keys->arr[i], values->arr[i]);
    }

    return d;
}


#endif