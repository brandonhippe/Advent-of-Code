#ifndef VECTOR_H
#define VECTOR_H


#include <stdlib.h>
#include <string.h>


struct vector *createVector();
void deleteVector(struct vector *v);
void append(struct vector *v, void *e);
void* pop(struct vector *v, int ix);
struct vector *slice(struct vector *v, int start, int end, int step);
struct vector *createCopy(struct vector *v, size_t (sizefun)(void *e));


struct vector {
    int len, cap;
    void **arr;
};


struct vector *createVector() {
    struct vector *v = (struct vector *)malloc(sizeof(struct vector));
    v->len = 0, v->cap = 1;
    v->arr = (void**)calloc(1, sizeof(void*));

    return v;
}


void deleteVector(struct vector *v) {
    free(v->arr);
    free(v);
}


void append(struct vector *v, void *e) {
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


void* pop(struct vector *v, int ix) {
    if (ix >= v->len) {
        exit(-1);
    }

    void *e = v->arr[ix];

    v->len--;

    if (v->len <= v->cap / 4) {
        v->cap /= 2;
    }

    void **newarr = (void**)calloc(v->cap, sizeof(void*));

    for (int i = 0; i <= v->len; i++) {
        newarr[i] = v->arr[i + (i >= ix ? 1 : 0)];
    }

    free(v->arr);
    v->arr = newarr;

    return e;
}


struct vector *slice(struct vector *v, int start, int end, int step) {
    if ((start < 0 || start >= v->len) || (end < 0 || end >= v->len) || step == 0) {
        return NULL;
    }

    struct vector *sliced = createVector();

    for (int i = start; (i < end && step > 0) || (i > end && step < 0); i += step) {
        append(sliced, v->arr[i]);
    }

    return sliced;
}


struct vector *createCopy(struct vector *v, size_t (sizefun)(void *e)) {
    struct vector *copy = createVector();

    for (int i = 0; i < v->len; i++) {
        void *newE = malloc(sizefun(v->arr[i]));
        memcpy(newE, v->arr[i], sizefun(v->arr[i]));
        append(copy, newE);
    }

    return copy;
}


#endif