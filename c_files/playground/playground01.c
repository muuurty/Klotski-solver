#include <stdio.h>

void fon(int a){
    printf("%d\n", a);
}
void meta_f(int a, void (*f)(int), int b){
    for (int i = 0; i<a; i++){
        (*f)(b);
    }
}

int fon2(int a){
    return a+5;
}
int meta_f2(int a, int (*f)(int), int b){
    return a*(*f)(b);
}

int main(void){
    // meta_f(45, *fon, 3);
    // printf("%d\n", meta_f2(45, *fon2, 3));
    for (int j = 15; j > -1; j--){
        printf("%d\n", j);
    }
    return 0;
}