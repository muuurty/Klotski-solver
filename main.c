#include <stdio.h>
#include <stdlib.h>

// int num_blocks = 10;

// class Size{
//     int[num_blocks] x;
//     int[num_blocks] y;
// }
// class Position{
//     int[num_blocks] x;
//     int[num_blocks] y;
// }
// Size size;
// size.x = {1,1,1,1,1,1,2,1,2,1};
// size.y = {2,1,1,2,1,1,1,2,2,2};
// Position position;
// position.x = {0,1,2,3,1,2,1,0,1,3};
// position.y = {0,0,0,0,1,1,2,3,3,3};
// grid_size[2] = {4, 5};

// int arr_max()

// bool is_empty(int *position[2][num_blocks], int xcheck, int ycheck){
//     bool empty = true;
//     int ymax = ycheck+1-arr_max(size[0]);
//     int xmax = xcheck+1-arr_max(size[1]);
//     if ycheck+1-arr_max(size[0]) > 0
//     for (int y = 0; y < ycheck+1-arr_max(size[0]); y++){}
//     return empty;
// }

void rec(int a){
    if (a > 0){
        rec(a-1);
    }
}

int main(void){
    // int *ptr = malloc(5 * sizeof(int));

    // if (ptr == NULL) {
    //     printf("Memory allocation failed\n");
    //     return 1;
    // }

    // for (int i = 0; i < 5; i++) {
    //     ptr[i] = i + 1;
    // }

    // for (int i = 0; i < 5; i++) {
    //     printf("%d ", ptr[i]);
    // }

    // free(ptr);

    rec(10000000);
    printf("Done\n");


    return 0;
}