#ifndef ADTHELP
#define ADTHELP


// Include headers
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>


// Function Prototypes
void *copyElement(void *e, size_t size);
size_t stringsize(void *e);
size_t charsize(void *e);
size_t intsize(void *e);
size_t doulbesize(void *e);


// Creates a copy of an element
void *copyElement(void *e, size_t size) {
    void *newE = calloc(1, size + 1);
    memcpy(newE, e, size);
    return newE;
}


// Returns size of string pointed to by void*
size_t stringsize(void *e) {
    return strlen((char*)e);
}


// Returns size of char pointed to by void*
size_t charsize(void *e) {
    return sizeof(char);
}


// Returns size of int pointed to by void*
size_t intsize(void *e) {
    return sizeof(int);
}


// Returns size of unsigned long pointed to by void*
size_t ulongsize(void *e) {
    return sizeof(unsigned long);
}


// Returns size of unsigned long long pointed to by void*
size_t ullsize(void *e) {
    return sizeof(unsigned long long);
}


// Returns size of double pointed to by void*
size_t doulbesize(void *e) {
    return sizeof(double);
}


#endif