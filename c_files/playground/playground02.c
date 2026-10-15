#include <stdio.h>
#include <stdlib.h>

void fon(int a){
    printf("%d\n", a);
}
void meta_f(int a, void (*f)(int), int b){
    for (int i = 0; i<a; i++){
        (*f)(b);
    }
}

int* fon2(int a){
    int *ptr = malloc(sizeof(int));
    ptr[0] = a;
    return ptr;
}
int* meta_f2(int a, void* (*f)(int)){
    return (*f)(a);
}

int main(void){
    int* a = meta_f2(3, *fon2);
    printf("%d\n", *a);
    free(a);
    return 0;
}